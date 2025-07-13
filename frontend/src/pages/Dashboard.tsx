import React, { useState } from 'react';
import { Upload, FileText, Brain, Settings } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import DocumentList from '../components/DocumentList';
import Statistics from '../components/Statistics';
import type { Document } from '../types';

const Dashboard: React.FC = () => {
    const [activeTab, setActiveTab] = useState<'overview' | 'documents' | 'upload'>('overview');
    const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

    const tabs = [
        { id: 'overview', name: 'Visão Geral', icon: FileText },
        { id: 'documents', name: 'Documentos', icon: FileText },
        { id: 'upload', name: 'Upload', icon: Upload },
    ];

    const handleDocumentSelect = (document: Document) => {
        setSelectedDocument(document);
        // Here you would typically navigate to a document detail page
        console.log('Selected document:', document);
    };

    const handleUploadComplete = (documentId: string) => {
        console.log('Upload completed:', documentId);
        // Optionally switch to documents tab or show success message
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-4">
                            <Brain className="h-8 w-8 text-primary-600" />
                            <h1 className="text-xl font-semibold text-gray-900">
                                Family Search OCR
                            </h1>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button className="btn-secondary">
                                <Settings className="h-4 w-4 mr-2" />
                                Configurações
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation Tabs */}
            <div className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <nav className="flex space-x-8">
                        {tabs.map((tab) => {
                            const IconComponent = tab.icon;
                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id as any)}
                                    className={`
                    flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm
                    ${activeTab === tab.id
                                            ? 'border-primary-500 text-primary-600'
                                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                        }
                  `}
                                >
                                    <IconComponent className="h-4 w-4" />
                                    <span>{tab.name}</span>
                                </button>
                            );
                        })}
                    </nav>
                </div>
            </div>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {activeTab === 'overview' && (
                    <div className="space-y-8">
                        {/* Statistics */}
                        <div>
                            <h2 className="text-lg font-medium text-gray-900 mb-6">
                                Estatísticas Gerais
                            </h2>
                            <Statistics />
                        </div>

                        {/* Recent Documents */}
                        <div>
                            <h2 className="text-lg font-medium text-gray-900 mb-6">
                                Documentos Recentes
                            </h2>
                            <DocumentList
                                onDocumentSelect={handleDocumentSelect}
                                className="max-w-4xl"
                            />
                        </div>
                    </div>
                )}

                {activeTab === 'documents' && (
                    <div>
                        <h2 className="text-lg font-medium text-gray-900 mb-6">
                            Todos os Documentos
                        </h2>
                        <DocumentList
                            onDocumentSelect={handleDocumentSelect}
                        />
                    </div>
                )}

                {activeTab === 'upload' && (
                    <div>
                        <h2 className="text-lg font-medium text-gray-900 mb-6">
                            Upload de Documentos
                        </h2>
                        <div className="max-w-2xl">
                            <FileUpload onUploadComplete={handleUploadComplete} />
                        </div>
                    </div>
                )}
            </main>

            {/* Success Message */}
            {selectedDocument && (
                <div className="fixed bottom-4 right-4 bg-green-50 border border-green-200 rounded-lg p-4 shadow-lg">
                    <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <p className="text-sm text-green-800">
                            Documento selecionado: {selectedDocument.filename}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard; 