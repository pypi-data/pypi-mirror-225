// Copyright 2021-2023 by Oxford Semantic Technologies Limited.

#include <algorithm>
#include <iostream>
#include <cstring>

#include <CRDFox/CRDFox.h>

static size_t getTriplesCount(CDataStoreConnection* dataStoreConnection, const char* queryDomain) {
    CParametersPtr parameters;
    CParameters_newEmptyParameters(&parameters);
    CParameters_setString(parameters, "fact-domain", queryDomain);

    CCursorPtr cursor;
    CDataStoreConnection_createCursor(dataStoreConnection, "SELECT ?X ?Y ?Z WHERE { ?X ?Y ?Z }", 34, parameters, &cursor);
    CDataStoreConnection_beginTransaction(dataStoreConnection, TRANSACTION_TYPE_READ_ONLY);
    size_t result = 0;
    size_t multiplicity;
    for (CCursor_open(cursor, 0, &multiplicity); multiplicity != 0; CCursor_advance(cursor, &multiplicity))
        result += multiplicity;
    CDataStoreConnection_rollbackTransaction(dataStoreConnection);
    return result;
}

void handleException(const CException* exception) {
    if (exception) {
        std::cout << "Exception:" << std::endl;
        std::cout << "Name: " << CException_getExceptionName(exception) << std::endl;
        std::cout << "What: " << CException_what(exception) << std::endl;
        exit(1);
    }
}

bool stdoutOutputStreamFlush(void* context) {
    return fflush(stdout) == 0;
}

bool stdoutOutputStreamWrite(void* context, const void* data, size_t numberOfBytesToWrite) {
    return fwrite(data, sizeof(char), numberOfBytesToWrite, stdout) == numberOfBytesToWrite;
}

struct MemoryInputStreamContext {

public:

    const char* const m_begin;
    const char* const m_afterEnd;
    const char* m_current;

    MemoryInputStreamContext(const char* const begin, const size_t size) :
        m_begin(begin),
        m_afterEnd(m_begin + size),
        m_current(m_begin)
    {
    }

};

bool memoryInputStreamRewind(void* context) {
    MemoryInputStreamContext& memoryInputStreamContext = *reinterpret_cast<MemoryInputStreamContext*>(context);
    memoryInputStreamContext.m_current = memoryInputStreamContext.m_begin;
    return false;
}

bool memoryInputStreamRead(void* context, void* data, size_t numberOfBytesToRead, size_t* bytesRead) {
    MemoryInputStreamContext& memoryInputStreamContext = *reinterpret_cast<MemoryInputStreamContext*>(context);
    const size_t bytesRemaining = static_cast<size_t>(memoryInputStreamContext.m_afterEnd - memoryInputStreamContext.m_current);
    numberOfBytesToRead = std::min<size_t>(numberOfBytesToRead, bytesRemaining);
    std::memcpy(data, memoryInputStreamContext.m_current, numberOfBytesToRead);
    *bytesRead = numberOfBytesToRead;
    memoryInputStreamContext.m_current += *bytesRead;
    return memoryInputStreamContext.m_current == memoryInputStreamContext.m_afterEnd;
}

int main() {
    handleException(CServer_startLocalServer(CParameters_getEmptyParameters()));

    CServer_createFirstLocalServerRole("", "");

    CServerConnection* serverConnection = nullptr;
    handleException(CServerConnection_newServerConnection("", "", &serverConnection));

    // We next specify how many threads the server should use during import of data and reasoning.
    std::cout << "Setting the number of threads..." << std::endl;
    handleException(CServerConnection_setNumberOfThreads(serverConnection, 2));

    // We the default value for the "type" perameter, which is "par-complex-nn".
    handleException(CServerConnection_createDataStore(serverConnection, "example", CParameters_getEmptyParameters()));

    // We connect to the data store.
    CDataStoreConnectionPtr dataStoreConnection;
    handleException(CServerConnection_newDataStoreConnection(serverConnection, "example", &dataStoreConnection));

    // We next import the RDF data into the store. At present, only Turtle/N-triples files are supported.
    // At the moment, please convert RDF/XML files into Turtle format to load into CRDFox.
    std::cout << "Importing RDF data..." << std::endl;

    // To show how to handle exceptions, try to import a file that does not exist.
    std::cout << "To show how to handle exceptions, try to import a file that does not exist." << std::endl;
    const CException* exception = CDataStoreConnection_importDataFromFile(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, "no_file.ttl", "text/turtle");
    if (exception) {
        std::cout << "Exception:" << std::endl;
        std::cout << "Name: " << CException_getExceptionName(exception) << std::endl;
        std::cout << "What: " <<  CException_what(exception) << std::endl;
    }

    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, "lubm1.ttl", "text/turtle"));

    // RDFox manages data in several fact domains.
    //
    // - The 'all' domain contains all facts -- that is, both the explicitly given and the derived facts.
    //
    // - The 'derived' domain contains the facts that were derived by reasoning, but were not explicitly given in the input.
    //
    // - The 'explicit' domain contains the facts that were explicitly given in the input.
    //
    // The domain must be specified in various places where queries are evaluated. If a query domain is not
    // specified, the 'all' domain is used.
    std::cout << "Number of tuples after import: " << getTriplesCount(dataStoreConnection, "all") << std::endl;

    // SPARQL queries can be evaluated in several ways. One option is to have the query result be written to
    // an output stream in one of the supported formats.
    struct COutputStream outputStream = { nullptr, &stdoutOutputStreamFlush, &stdoutOutputStreamWrite };
    CStatementResult statementResult;
    handleException(CDataStoreConnection_evaluateStatement(dataStoreConnection, "SELECT DISTINCT ?Y WHERE { ?X ?Y ?Z }", 37, CParameters_getEmptyParameters(), &outputStream, "application/sparql-results+json", &statementResult));
    std::cout << "Query produced " << statementResult.numberOfQueryAnswers << " answers." << std::endl;

    // We now add the ontology and the custom rules to the data.

    // In this example, the rules are kept in a file separate from the ontology. JRDFox supports
    // SWRL rules, so it is possible to store the rules into the OWL ontology.

    std::cout << "Adding the ontology to the store..." << std::endl;
    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, "univ-bench.owl", "text/owl-functional"));

    std::cout << "Importing rules from a file..." << std::endl;
    handleException(CDataStoreConnection_importDataFromFile(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, "additional-rules.txt", ""));

    std::cout << "Number of tuples after materialization: " << getTriplesCount(dataStoreConnection, "all") <<std::endl;

    // We now evaluate the same query as before, but we do so using a cursor, which provides us with
    // programmatic access to individual query results.

    CCursorPtr cursor;
    CDataStoreConnection_createCursor(dataStoreConnection, "SELECT DISTINCT ?Y WHERE { ?X ?Y ?Z }", 37, CParameters_getEmptyParameters(), &cursor);

    int numberOfRows = 0;
    std::cout << "\n=======================================================================================" << std::endl;

    size_t arity;
    CCursor_getArity(cursor, &arity);
    const char* variableName;
    for (size_t termIndex = 0; termIndex < arity; ++termIndex) {
        if (termIndex != 0)
            std::cout << "  ";
        // For each variable, we print the name.
        CCursor_getAnswerVariableName(cursor, termIndex, &variableName);
        std::cout << '?' << variableName;
    }
    printf("\n---------------------------------------------------------------------------------------\n");

    size_t multiplicity;
    // We iterate through the result tuples.
    for (CCursor_open(cursor, 0, &multiplicity); multiplicity != 0; CCursor_advance(cursor, &multiplicity)) {
        ++numberOfRows;
        // We iterate through the terms of each tuple.
        for (size_t termIndex = 0; termIndex < arity; ++termIndex) {
            if (termIndex != 0)
                std::cout << "  ";
            // For each term, we retrieve the lexical form and the data type of the term.
            CDatatypeID datatypeID;
            char lexicalFormBuffer[1024];
            size_t lexicalFormSize = 0;
            bool resourceResolved = false;
            CCursor_appendResourceLexicalForm(cursor, termIndex, lexicalFormBuffer, sizeof(lexicalFormBuffer), &lexicalFormSize, &datatypeID, &resourceResolved);
            if (lexicalFormSize >= sizeof(lexicalFormBuffer)) {
                CCursor_getAnswerVariableName(cursor, termIndex, &variableName);
                std::cout << "Warning: the lexical form for the term bound to variable ?" << variableName << " on row " << numberOfRows << " was truncated from " << lexicalFormSize << " to " << sizeof(lexicalFormBuffer) - 1 << " characters." << std::endl;
                lexicalFormBuffer[sizeof(lexicalFormBuffer) - 1] = '\0';
            }
            else
                lexicalFormBuffer[lexicalFormSize] = '\0';
            std::cout << lexicalFormBuffer;
        }
        std::cout << std::endl;
    }
    std::cout << "---------------------------------------------------------------------------------------" << std::endl;
    std::cout << "  The number of rows returned: " << numberOfRows <<std::endl;
    std::cout << "=======================================================================================\n" << std::endl;

    // RDFox supports incremental reasoning. One can import facts into the store incrementally by
    // calling importDataFromFile(dataStoreConnection, ...) with additional argument UPDATE_TYPE_ADDITION.
    std::cout << "Importing triples for incremental reasoning..." << std::endl;
    CDataStoreConnection_importDataFromFile(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, "lubm1-new.ttl", "text/turtle");

    // Adding the rules/facts changes the number of triples. Note that the store is updated incrementally.
    std::cout << "Number of tuples after addition: " << getTriplesCount(dataStoreConnection, "all") << '\n' << std::endl;

    // Content can be imported from buffers or from streams as well as from file. Here we will add one triple stored
    // in a c string using CDataStoreConnection_importDataFromBuffer and then remove the same content using an in-memory
    // implementation of CInputStream for the same c string. Each time we will re-count the triples for comparison.
    std::cout << "Adding hard-coded triple..." << std::endl;
    const char* hardCodedTriple = "<http://example.com/subject> <http://example.com/predicate> <http://example.com/object> .";
    const size_t hardCodedTripleLength = std::strlen(hardCodedTriple);
    CDataStoreConnection_importDataFromBuffer(dataStoreConnection, nullptr, UPDATE_TYPE_ADDITION, reinterpret_cast<const byte_t*>(hardCodedTriple), hardCodedTripleLength, "text/turtle");
    std::cout << "Number of tuples after adding hard-coded triple: " << getTriplesCount(dataStoreConnection, "all") << '\n' << std::endl;
    std::cout << "Removing hard-coded triple..." << std::endl;
    MemoryInputStreamContext memoryInputStreamContext(hardCodedTriple, hardCodedTripleLength);
    struct CInputStream inputStream = { &memoryInputStreamContext, &memoryInputStreamRewind, &memoryInputStreamRead };
    CDataStoreConnection_importData(dataStoreConnection, nullptr, UPDATE_TYPE_DELETION, &inputStream, "https://rdfox.com/default-base-iri/", "text/turtle");
    std::cout << "Number of tuples after removing hard-coded triple: " << getTriplesCount(dataStoreConnection, "all") << '\n' << std::endl;

    // One can export the facts from the current store into a file as follows.
    std::cout << "Exporting facts to file 'final-facts.ttl'..." << std::endl;
    CParametersPtr parameters;
    CParameters_newEmptyParameters(&parameters);
    CParameters_setString(parameters, "fact-domain", "all");
    CDataStoreConnection_exportDataToFile(dataStoreConnection, "final-facts.ttl", "application/n-triples", parameters);

    std::cout << "This is the end of the example!" << std::endl;
    return 0;
}
