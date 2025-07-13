import React, { useState } from 'react';
import { File, Eye, Trash2, Download, Calendar, Clock } from 'lucide-react';
import { useDocuments, useDeleteDocument } from '../hooks/useDocuments';
import type { Document } from '../types';

interface DocumentListProps {
    onDocumentSelect?: (document: Document) => void;
    className?: string;
}

const DocumentList: React.FC<DocumentListProps> = ({ onDocumentSelect, className = '' }) => {
    const [page, setPage] = useState(1);
    const [limit] = useState(10);

    const { data: documentsData, isLoading, error } = useDocuments(page, limit);
    const deleteMutation = useDeleteDocument();

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('pt-BR', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const formatFileSize = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const getStatusColor = (status: Document['status']) => {
        switch (status) {
            case 'completed':
                return 'bg-green-100 text-green-800';
            case 'processing':
                return 'bg-yellow-100 text-yellow-800';
            case 'error':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Document['status']) => {
        switch (status) {
            case 'completed':
                return 'Concluído';
            case 'processing':
                return 'Processando';
            case 'error':
                return 'Erro';
            default:
                return 'Desconhecido';
        }
    };

    const handleDelete = (id: string) => {
        if (window.confirm('Tem certeza que deseja excluir este documento?')) {
            deleteMutation.mutate(id);
        }
    };

    if (isLoading) {
        return (
            <div className={`space-y-4 ${className}`}>
                {[...Array(5)].map((_, i) => (
                    <div key={i} className="card animate-pulse">
                        <div className="flex items-center space-x-4">
                            <div className="w-10 h-10 bg-gray-200 rounded"></div>
                            <div className="flex-1 space-y-2">
                                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (error) {
        return (
            <div className={`card ${className}`}>
                <div className="text-center text-red-600">
                    <p>Erro ao carregar documentos. Tente novamente.</p>
                </div>
            </div>
        );
    }

    if (!documentsData?.items || documentsData.items.length === 0) {
        return (
            <div className={`card text-center ${className}`}>
                <File className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Nenhum documento encontrado
                </h3>
                <p className="text-gray-500">
                    Faça upload de documentos para começar a análise.
                </p>
            </div>
        );
    }

    return (
        <div className={`space-y-4 ${className}`}>
            {/* Documents List */}
            <div className="space-y-3">
                {documentsData.items.map((document) => (
                    <div key={document.id} className="card hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4 flex-1">
                                <div className="flex-shrink-0">
                                    <File className="h-8 w-8 text-gray-400" />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center space-x-2 mb-1">
                                        <h3 className="text-sm font-medium text-gray-900 truncate">
                                            {document.filename}
                                        </h3>
                                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(document.status)}`}>
                                            {getStatusText(document.status)}
                                        </span>
                                    </div>
                                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                                        <span className="flex items-center space-x-1">
                                            <Calendar className="h-3 w-3" />
                                            <span>{formatDate(document.created_at)}</span>
                                        </span>
                                        <span>{formatFileSize(document.file_size)}</span>
                                        <span className="flex items-center space-x-1">
                                            <Clock className="h-3 w-3" />
                                            <span>Confiança: {Math.round(document.confidence_score * 100)}%</span>
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center space-x-2">
                                <button
                                    onClick={() => onDocumentSelect?.(document)}
                                    className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                                    title="Visualizar documento"
                                >
                                    <Eye className="h-4 w-4" />
                                </button>
                                <button
                                    onClick={() => handleDelete(document.id)}
                                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                    title="Excluir documento"
                                    disabled={deleteMutation.isPending}
                                >
                                    <Trash2 className="h-4 w-4" />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Pagination */}
            {documentsData.total_pages > 1 && (
                <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                        Mostrando {((page - 1) * limit) + 1} a {Math.min(page * limit, documentsData.total)} de {documentsData.total} documentos
                    </div>
                    <div className="flex items-center space-x-2">
                        <button
                            onClick={() => setPage(page - 1)}
                            disabled={page === 1}
                            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Anterior
                        </button>
                        <span className="text-sm text-gray-700">
                            Página {page} de {documentsData.total_pages}
                        </span>
                        <button
                            onClick={() => setPage(page + 1)}
                            disabled={page === documentsData.total_pages}
                            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Próxima
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DocumentList; 