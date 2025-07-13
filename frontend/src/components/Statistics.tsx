import React from 'react';
import {
    FileText,
    CheckCircle,
    TrendingUp,
    Brain,
    Clock,
    Target
} from 'lucide-react';
import { useStatistics } from '../hooks/useStatistics';

const Statistics: React.FC = () => {
    const { data: stats, isLoading, error } = useStatistics();

    if (isLoading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                    <div key={i} className="card animate-pulse">
                        <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                            <div className="flex-1">
                                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                                <div className="h-6 bg-gray-200 rounded w-1/3"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (error || !stats) {
        return (
            <div className="card">
                <div className="text-center text-red-600">
                    <p>Erro ao carregar estatísticas.</p>
                </div>
            </div>
        );
    }

    const statCards = [
        {
            title: 'Total de Documentos',
            value: stats.total_documents,
            icon: FileText,
            color: 'text-blue-600',
            bgColor: 'bg-blue-50',
        },
        {
            title: 'Documentos Processados',
            value: stats.processed_documents,
            icon: CheckCircle,
            color: 'text-green-600',
            bgColor: 'bg-green-50',
        },
        {
            title: 'Documentos Hoje',
            value: stats.documents_today,
            icon: Clock,
            color: 'text-yellow-600',
            bgColor: 'bg-yellow-50',
        },
        {
            title: 'Confiança Média',
            value: `${Math.round(stats.average_confidence * 100)}%`,
            icon: TrendingUp,
            color: 'text-purple-600',
            bgColor: 'bg-purple-50',
        },
        {
            title: 'Total de Correções',
            value: stats.total_corrections,
            icon: Target,
            color: 'text-indigo-600',
            bgColor: 'bg-indigo-50',
        },
        {
            title: 'Precisão da IA',
            value: `${Math.round(stats.ai_accuracy * 100)}%`,
            icon: Brain,
            color: 'text-pink-600',
            bgColor: 'bg-pink-50',
        },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {statCards.map((stat, index) => {
                const IconComponent = stat.icon;
                return (
                    <div key={index} className="card hover:shadow-md transition-shadow">
                        <div className="flex items-center space-x-4">
                            <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                                <IconComponent className={`h-6 w-6 ${stat.color}`} />
                            </div>
                            <div className="flex-1">
                                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default Statistics; 