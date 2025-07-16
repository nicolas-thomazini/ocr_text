import React from 'react';
import { useDocuments, useDeleteDocument, useProcessDocument } from '../hooks/useDocuments';
import type { Document } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const DocumentDashboard: React.FC = () => {
    const { data: documentsData, isLoading, error } = useDocuments(1, 100);
    const deleteMutation = useDeleteDocument();
    const processMutation = useProcessDocument();

    const handleDelete = (id: string) => {
        if (window.confirm('Tem certeza que deseja excluir este documento?')) {
            deleteMutation.mutate(id);
        }
    };

    const handleProcess = (id: string) => {
        processMutation.mutate(id);
    };

    if (isLoading) return <div>Carregando documentos...</div>;
    if (error) return <div>Erro ao carregar documentos.</div>;
    if (!documentsData?.items || documentsData.items.length === 0) return <div>Nenhum documento encontrado.</div>;

    return (
        <div className="space-y-6">
            {documentsData.items.map((doc: Document) => {
                console.log('Status do documento:', doc.status);
                return (
                    <div key={doc.id} className="card p-4 flex flex-col md:flex-row gap-4 items-start md:items-center">
                        <div className="flex flex-col items-center gap-2">
                            <span className="text-xs text-gray-500">Original</span>
                            <img
                                src={`${API_BASE_URL}/uploads/${doc.filename}`}
                                alt="Original"
                                className="w-40 h-auto border rounded shadow"
                                onError={e => (e.currentTarget.style.display = 'none')}
                            />
                        </div>
                        <div className="flex flex-col items-center gap-2">
                            <span className="text-xs text-gray-500">Pré-processada</span>
                            <img
                                src={`${API_BASE_URL}/preprocessed-images/${doc.filename}`}
                                alt="Pré-processada"
                                className="w-40 h-auto border rounded shadow"
                                onError={e => (e.currentTarget.style.display = 'none')}
                            />
                        </div>
                        <div className="flex-1">
                            <div className="mb-2">
                                <span className="font-semibold">Arquivo:</span> {doc.filename}
                            </div>
                            <div className="mb-2">
                                <span className="font-semibold">Status:</span> {doc.status}
                            </div>
                            <div className="mb-2">
                                <span className="font-semibold">Data de Upload:</span>
                                {doc.upload_date && !isNaN(Date.parse(doc.upload_date))
                                    ? new Date(doc.upload_date).toLocaleString('pt-BR')
                                    : 'N/A'}

                            </div>
                            <div className="mb-2">
                                <span className="font-semibold">Confiança:</span>
                                {typeof doc.confidence_score === 'number' && doc.confidence_score > 0
                                    ? `${Math.round(doc.confidence_score)}%`
                                    : 'N/A'}

                            </div>
                            <div className="mb-2">
                                <span className="font-semibold">Texto OCR:</span>
                                <div className="bg-gray-100 rounded p-2 mt-1 text-xs max-h-32 overflow-auto whitespace-pre-line">
                                    {doc.original_text || 'Nenhum texto extraído.'}
                                </div>
                            </div>
                            {(doc.status === 'uploaded' || doc.status === 'error') && (
                                <button
                                    onClick={() => handleProcess(doc.id)}
                                    className="mt-2 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 mr-2"
                                    disabled={processMutation.isPending}
                                >
                                    {processMutation.isPending ? 'Processando...' : 'Processar OCR'}
                                </button>
                            )}
                            <button
                                onClick={() => handleDelete(doc.id)}
                                className="mt-2 px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                                disabled={deleteMutation.isPending}
                            >
                                Excluir
                            </button>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default DocumentDashboard; 