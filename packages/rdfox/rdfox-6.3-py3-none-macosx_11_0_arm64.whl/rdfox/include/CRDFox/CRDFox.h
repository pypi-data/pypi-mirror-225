// Copyright 2021-2023 by Oxford Semantic Technologies Limited.

#ifndef CRDFOX_H_
#define CRDFOX_H_

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#ifdef __cplusplus

#include <cstddef>

extern "C" {
#endif

#ifdef _WIN64
    #ifdef CRDFOX_EXPORT
        #define CRDFOX __declspec(dllexport)
    #else
        #define CRDFOX __declspec(dllimport)
    #endif
#else
    #define CRDFOX
#endif

typedef uint8_t byte_t;
typedef uint8_t CDatatypeID;

extern const char* const GUESS_FORMAT_NAME;

typedef enum { UPDATE_TYPE_ADDITION = 0, UPDATE_TYPE_ADDITION_UPDATE_PREFIXES = 11, UPDATE_TYPE_DELETION = 19 } CUpdateType;

typedef enum { TRANSACTION_TYPE_EXCLUSIVE = 0, TRANSACTION_TYPE_READ_WRITE = 1, TRANSACTION_TYPE_READ_ONLY = 2 } CTransactionType;

typedef enum { TRANSACTION_STATE_EXCLUSIVE = 0, TRANSACTION_STATE_READ_WRITE = 1, TRANSACTION_STATE_READ_ONLY = 2, TRANSACTION_STATE_NONE = 3 } CTransactionState;

typedef struct {
    bool statementTypeSupportsUserQuery;
    size_t numberOfQueryAnswers;
    size_t totalNumberOfQueryAnswers;
    bool statementTypeSupportsDeletions;
    size_t numberOfAttemptedDeletions;
    size_t numberOfDeletions;
    bool statementTypeSupportsInsertions;
    size_t numberOfAttemptedInsertions;
    size_t numberOfInsertions;
} CStatementResult;

typedef struct {
    unsigned char __dummy;
} CException;

typedef struct {
    unsigned char __dummy;
} CPrefixes;

typedef struct {
    unsigned char __dummy;
} CParameters;

typedef struct {
    unsigned char __dummy;
} CServerConnection;

typedef struct {
    unsigned char __dummy;
} CDataStoreConnection;

typedef struct {
    unsigned char __dummy;
} CCursor;

typedef struct COutputStream {
    void* context;
    bool (*flushFn)(void* context);
    bool (*writeFn)(void* context, const void* data, size_t numberOfBytesToWrite);
} COutputStream;

typedef struct CInputStream {
    void* context;
    bool (*rewindFn)(void* context);
    bool (*readFn)(void* context, void* data, size_t numberOfBytesToRead, size_t* bytesRead);
} CInputStream;

extern const COutputStream* const RDFOX_STDOUT;

// ------------------------
// CException
// ------------------------

CRDFOX const CException* CException_duplicate(const CException* sourceException, CException** resultException);

CRDFOX void CException_destroy(CException* exception);

CRDFOX const char* CException_what(const CException* exception);

CRDFOX bool CException_isRDFoxException(const CException* exception);

CRDFOX const char* CException_getExceptionName(const CException* exception);

CRDFOX const char* CRDFoxException_getMessage(const CException* exception);

CRDFOX size_t CRDFoxException_getNumberOfCauses(const CException* exception);

CRDFOX const CException* CRDFoxException_getCause(const CException* exception, size_t causeIndex);


// ------------------------
// CParameters
// ------------------------

CRDFOX const CParameters* CParameters_getEmptyParameters(void);

CRDFOX void CParameters_destroy(CParameters* parameters);

CRDFOX const CException* CParameters_newEmptyParameters(CParameters** parameters);

CRDFOX const CException* CParameters_setString(CParameters* parameters, const char* key, const char* value);

CRDFOX const CException* CParameters_getString(const CParameters* parameters, const char* key, const char* const defaultValue, const char** string);


// ------------------------
// CPrefixes
// ------------------------

typedef enum { PREFIXES_INVALID_PREFIX_NAME, PREFIXES_NO_CHANGE, PREFIXES_REPLACED_EXISTING, PREFIXES_DECLARED_NEW } CPrefixes_DeclareResult;

CRDFOX const CPrefixes* CPrefixes_getEmptyPrefixes(void);

CRDFOX const CPrefixes* CPrefixes_getDefaultPrefixes(void);

CRDFOX void CPrefixes_destroy(CPrefixes* prefixes);

CRDFOX const CException* CPrefixes_newEmptyPrefixes(CPrefixes** prefixes);

CRDFOX const CException* CPrefixes_newDefaultPrefixes(CPrefixes** prefixes);

CRDFOX const CException* CPrefixes_declareStandardPrefixes(CPrefixes* prefixes);

CRDFOX const CException* CPrefixes_declarePrefix(CPrefixes* prefixes, const char* prefixName, const char* prefixIRI, CPrefixes_DeclareResult* declareResult);

CRDFOX const CException* CPrefixes_undeclarePrefix(CPrefixes* prefixes, const char* prefixName, bool* changed);

CRDFOX const CException* CPrefixes_getPrefix(const CPrefixes* prefixes, const char* prefixName, const char** prefixIRI);


// ------------------------
// CServer
// ------------------------

CRDFOX const CException* CServer_startLocalServer(const CParameters* parameters);

CRDFOX const CException* CServer_getNumberOfLocalServerRoles(size_t* numberOfRoles);

CRDFOX const CException* CServer_createFirstLocalServerRole(const char* firstRoleName, const char* password);

CRDFOX void CServer_stopLocalServer(void);


// ------------------------
// CServerConnection
// ------------------------

CRDFOX const CException* CServerConnection_newServerConnection(const char* roleName, const char* password, CServerConnection** serverConnection);

CRDFOX void CServerConnection_destroy(CServerConnection* serverConnection);

// Connection management

CRDFOX const CException* CServerConnection_interrupt(CServerConnection* serverConnection);

CRDFOX const CException* CServerConnection_duplicate(CServerConnection* serverConnection, CServerConnection** outputServerConnection);

// Server properties

CRDFOX const CException* CServerConnection_getVersion(CServerConnection* serverConnection, const char** version);

CRDFOX const CException* CServerConnection_getGitSHA(CServerConnection* serverConnection, const char** gitSHA);

CRDFOX const CException* CServerConnection_getMemoryUse(CServerConnection* serverConnection, size_t* maxUsedBytes, size_t* availableBytes);

CRDFOX const CException* CServerConnection_setMaxMemoryUse(CServerConnection* serverConnection, const size_t maxUsedBytes);

CRDFOX const CException* CServerConnection_getNumberOfThreads(CServerConnection* serverConnection, size_t* numberOfThreads);

CRDFOX const CException* CServerConnection_setNumberOfThreads(CServerConnection* serverConnection, size_t numberOfThreads);

// Data store management

CRDFOX const CException* CServerConnection_createDataStore(CServerConnection* serverConnection, const char* dataStoreName, const CParameters* dataStoreParameters);

CRDFOX const CException* CServerConnection_deleteDataStore(CServerConnection* serverConnection, const char* dataStoreName);

CRDFOX const CException* CServerConnection_newDataStoreConnection(CServerConnection* serverConnection, const char* dataStoreName, CDataStoreConnection** dataStoreConnection);

// Role management


// ------------------------
// CDataStoreConnection
// ------------------------

CRDFOX const CException* CDataStoreConnection_newDataStoreConnection(const char* dataStoreName, const char* roleName, const char* password, CDataStoreConnection** dataStoreConnection);

CRDFOX void CDataStoreConnection_destroy(CDataStoreConnection* dataStoreConnection);

// Connection management

CRDFOX const CException* CDataStoreConnection_interrupt(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_duplicate(CDataStoreConnection* dataStoreConnection, CDataStoreConnection** outputDataStoreConnection);

// Data store properties

CRDFOX const CException* CDataStoreConnection_getName(CDataStoreConnection* dataStoreConnection, const char** name);

CRDFOX const CException* CDataStoreConnection_getUniqueID(CDataStoreConnection* dataStoreConnection, const char** uniqueID);

// Base IRI management

CRDFOX const CException* CDataStoreConnection_getBaseIRI(CDataStoreConnection* dataStoreConnection, char* baseIRIBuffer, size_t baseIRIBufferSize, size_t* baseIRIBufferRequiredLength);

CRDFOX const CException* CDataStoreConnection_setBaseIRI(CDataStoreConnection* dataStoreConnection, const char* baseIRI, bool* changed);

// Prefixes management

CRDFOX const CException* CDataStoreConnection_getPrefixes(CDataStoreConnection* dataStoreConnection, CPrefixes* prefixes);

CRDFOX const CException* CDataStoreConnection_setPrefixes(CDataStoreConnection* dataStoreConnection, const CPrefixes* prefixes);

CRDFOX const CException* CDataStoreConnection_setPrefix(CDataStoreConnection* dataStoreConnection, const char* prefixName, const char* prefixIRI, bool* changed);

CRDFOX const CException* CDataStoreConnection_unsetPrefix(CDataStoreConnection* dataStoreConnection, const char* prefixName, bool* changed);

// Data source management

// Tuple table management

// Statistics management

// Commit procedure management

CRDFOX const CException* CDataStoreConnection_setCommitProcedure(CDataStoreConnection* dataStoreConnection, const char* commitProcedure, bool* changed);

CRDFOX const CException* CDataStoreConnection_clearCommitProcedure(CDataStoreConnection* dataStoreConnection, bool* changed);

// Transaction management

CRDFOX const CException* CDataStoreConnection_setNextOperationMustMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getNextOperationMustMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_setNextOperationMustNotMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getNextOperationMustNotMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getDataStoreVersionAfterLastOperation(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getTransactionState(CDataStoreConnection* dataStoreConnection, CTransactionState* transactionState);

CRDFOX const CException* CDataStoreConnection_transactionRequiresRollback(CDataStoreConnection* dataStoreConnection, bool* transactionRequiresRollback);

CRDFOX const CException* CDataStoreConnection_beginTransaction(CDataStoreConnection* dataStoreConnection, CTransactionType transactionType);

CRDFOX const CException* CDataStoreConnection_commitTransaction(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_rollbackTransaction(CDataStoreConnection* dataStoreConnection);

// Various operations on the data store

CRDFOX const CException* CDataStoreConnection_clear(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_clearRulesAxiomsExplicateFacts(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_compact(CDataStoreConnection* dataStoreConnection, const bool deleteRedundantFiles);

// Data import/export

CRDFOX const CException* CDataStoreConnection_exportData(CDataStoreConnection* dataStoreConnection, const COutputStream* outputStream, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_exportDataToBuffer(CDataStoreConnection* dataStoreConnection, char* buffer, size_t bufferSize, size_t* resultSize, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_exportDataToFile(CDataStoreConnection* dataStoreConnection, const char* filePath, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_importData(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, const CInputStream* inputStream, const char* baseIRI, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromBuffer(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, const byte_t* buffer, size_t bufferLength, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromFile(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, const char* filePath, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromURI(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, const char* uri, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importAxiomsFromTriples(CDataStoreConnection* dataStoreConnection, const char* sourceGraphName, bool translateAssertions, const char* destinationGraphName, CUpdateType updateType);

// Management of the axioms

// Management of the rules

// Management of the materialization

// Explanation

// Query & update evaluation

CRDFOX const CException* CDataStoreConnection_createCursor(CDataStoreConnection* dataStoreConnection, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, CCursor** cursor);

CRDFOX const CException* CDataStoreConnection_evaluateQuery(CDataStoreConnection* dataStoreConnection,const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, const COutputStream* outputStream, const char* queryAnswerFormatName, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateQueryToBuffer(CDataStoreConnection* dataStoreConnection, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, char* buffer, size_t bufferSize, size_t* resultSize, const char* queryAnswerFormatName, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateQueryToFile(CDataStoreConnection* dataStoreConnection, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, const char* filePath, const char* queryAnswerFormatName, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateUpdate(CDataStoreConnection* dataStoreConnection, const char* updateText, const size_t updateTextLength, const CParameters* compilationParameters, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatement(CDataStoreConnection* dataStoreConnection, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, const COutputStream* outputStream, const char* queryAnswerFormatName, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatementToBuffer(CDataStoreConnection* dataStoreConnection, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, char* buffer, size_t bufferSize, size_t* resultSize, const char* queryAnswerFormatName, CStatementResult* statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatementToFile(CDataStoreConnection* dataStoreConnection, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, const char* filePath, const char* queryAnswerFormatName, CStatementResult* statementResult);

// Saving to binary format


// ------------------------
// CCursor
// ------------------------

CRDFOX void CCursor_destroy(CCursor* cursor);

CRDFOX const CException* CCursor_getDataStoreConnection(CCursor* cursor, CDataStoreConnection** dataStoreConnection);

CRDFOX const CException* CCursor_isAskQuery(CCursor* cursor, bool* isAskQuery);

CRDFOX const CException* CCursor_getArity(CCursor* cursor, size_t* arity);

CRDFOX const CException* CCursor_getAnswerVariableName(CCursor* cursor, size_t variableIndex, const char** answerVariableName);

CRDFOX const CException* CCursor_open(CCursor* cursor, size_t skipToOffset, size_t* multiplicity);

CRDFOX const CException* CCursor_canAdvance(CCursor* cursor, bool* canAdvance);

CRDFOX const CException* CCursor_advance(CCursor* cursor, size_t* multiplicity);

CRDFOX const CException* CCursor_getCurrentOffset(CCursor* cursor, size_t* currentOffset);

CRDFOX const CException* CCursor_getCurrentMultiplicity(CCursor* cursor, size_t* currentMultiplicity);

CRDFOX const CException* CCursor_produceQueryAnswers(CCursor* cursor, const COutputStream* outputStream, const char* queryAnswerFormatName, size_t maxNumberOfAnswersToProduce, size_t* numberOfProducedAnswers);

CRDFOX const CException* CCursor_produceQueryAnswersToBuffer(CCursor* cursor, char* buffer, size_t bufferSize, size_t* resultSize, const char* queryAnswerFormatName, size_t maxNumberOfAnswersToProduce, size_t* numberOfProducedAnswers);

CRDFOX const CException* CCursor_produceQueryAnswersToFile(CCursor* cursor, const char* filePath, const char* queryAnswerFormatName, size_t maxNumberOfAnswersToProduce, size_t* numberOfProducedAnswers);

CRDFOX const CException* CCursor_stop(CCursor* cursor);

CRDFOX const CException* CCursor_getDatatypeID(CCursor* cursor, size_t variableIndex, CDatatypeID* datatypeID);

CRDFOX const CException* CCursor_appendResourceLexicalForm(CCursor* cursor, size_t variableIndex, char* buffer, size_t bufferSize, size_t* lexicalFormSize, CDatatypeID* datatypeID, bool* resourceResolved);

CRDFOX const CException* CCursor_appendResourceTurtleLiteral(CCursor* cursor, size_t variableIndex, char* buffer, size_t bufferSize, size_t* turtleLiteralSize, CDatatypeID* datatypeID, bool* resourceResolved);

#ifdef __cplusplus
}

template<class T, void (*destroyer)(T*)>
class CObjectPtr {

protected:

    T* m_object;

    struct AddressWrapper {
        CObjectPtr<T, destroyer>* m_objectPointer;
        T* m_temporary;

        inline explicit AddressWrapper(CObjectPtr<T, destroyer>* const objectPointer) noexcept :
            m_objectPointer(objectPointer),
            m_temporary(objectPointer->m_object)
        {
        }

        AddressWrapper(const AddressWrapper& other) = delete;

        inline AddressWrapper(AddressWrapper&& other) :
            m_objectPointer(other.m_objectPointer),
            m_temporary(other.m_temporary)
        {
            other.m_objectPointer = nullptr;
            other.m_temporary = nullptr;
        }

        AddressWrapper& operator=(const AddressWrapper& other) = delete;

        AddressWrapper& operator=(AddressWrapper&& other) = delete;

        inline ~AddressWrapper() {
            if (m_objectPointer == nullptr)
                destroyer(m_temporary);
            else if (m_temporary != m_objectPointer->m_object) {
                destroyer(m_objectPointer->m_object);
                m_objectPointer->m_object = m_temporary;
            }
        }

        inline operator T**() && noexcept {
            return &m_temporary;
        }

        inline operator CObjectPtr<T, destroyer>*() const {
            return m_objectPointer;
        }

    };

public:

    inline explicit CObjectPtr(T* object = nullptr) noexcept :
        m_object(object)
    {
    }

    inline CObjectPtr(const CObjectPtr<T, destroyer>& other) = delete;

    inline CObjectPtr(CObjectPtr<T, destroyer>&& other) noexcept : m_object(other.m_object) {
        other.m_object = nullptr;
    }

    CObjectPtr<T, destroyer>& operator=(const CObjectPtr<T, destroyer>& other) = delete;

    inline CObjectPtr<T, destroyer>& operator=(CObjectPtr<T, destroyer>&& other) noexcept {
        if (&m_object != &other.m_object) {
            destroyer(m_object);
            m_object = other.m_object;
            other.m_object = nullptr;
        }
        return *this;
    }

    inline ~CObjectPtr() {
        destroyer(m_object);
    }

    inline void swap(CObjectPtr<T, destroyer>& other) noexcept {
        T* object = m_object;
        m_object = other.m_object;
        other.m_object = object;
    }

    inline void reset(T* const object = nullptr) noexcept {
        destroyer(m_object);
        m_object = object;
    }

    inline T* release() noexcept {
        T* object = m_object;
        m_object = nullptr;
        return object;
    }

    inline T* get() const noexcept {
        return m_object;
    }

    inline operator T*() const noexcept {
        return m_object;
    }

    inline AddressWrapper operator&() noexcept {
        return AddressWrapper(this);
    }

    inline explicit operator bool() const noexcept {
        return m_object != nullptr;
    }

};

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator==(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() == object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator!=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() != object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator<(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() < object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator<=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() <= object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator>(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() > object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator>=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() >= object2.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator==(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() == nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator==(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr == object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator!=(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() != nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator!=(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr != object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator<(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() < nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator<(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr < object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator<=(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() <= nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator<=(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr <= object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator>(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() > nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator>(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr > object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator>=(const CObjectPtr<T, destroyer>& object, std::nullptr_t) {
    return object.get() >= nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator>=(std::nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr >= object.get();
}

namespace std {

    template<class T, void (*destroyer)(T*)>
    inline void swap(CObjectPtr<T, destroyer>& pointer1, CObjectPtr<T, destroyer>& pointer2) noexcept {
        pointer1.swap(pointer2);
    }

}

typedef CObjectPtr<CException, CException_destroy> CExceptionPtr;
typedef CObjectPtr<CPrefixes, CPrefixes_destroy> CPrefixesPtr;
typedef CObjectPtr<CParameters, CParameters_destroy> CParametersPtr;
typedef CObjectPtr<CServerConnection, CServerConnection_destroy> CServerConnectionPtr;
typedef CObjectPtr<CDataStoreConnection, CDataStoreConnection_destroy> CDataStoreConnectionPtr;
typedef CObjectPtr<CCursor, CCursor_destroy> CCursorPtr;

#endif

#endif // CRDFOX_H_
