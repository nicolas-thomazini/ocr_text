import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiService from '../services/api';
import type { AICorrection, AIModel } from '../types';

export const useAICorrections = (documentId: string) => {
    return useQuery({
        queryKey: ['ai-corrections', documentId],
        queryFn: () => apiService.getAICorrections(documentId),
        enabled: !!documentId,
        staleTime: 2 * 60 * 1000, // 2 minutes
    });
};

export const useCreateAICorrection = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (documentId: string) => apiService.createAICorrection(documentId),
        onSuccess: (data, documentId) => {
            // Invalidate and refetch AI corrections for this document
            queryClient.invalidateQueries({ queryKey: ['ai-corrections', documentId] });
        },
    });
};

export const useUpdateCorrection = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ correctionId, corrections }: { correctionId: string; corrections: any[] }) =>
            apiService.updateCorrection(correctionId, corrections),
        onSuccess: () => {
            // Invalidate all AI corrections queries
            queryClient.invalidateQueries({ queryKey: ['ai-corrections'] });
        },
    });
};

export const useAIModel = () => {
    return useQuery({
        queryKey: ['ai-model'],
        queryFn: () => apiService.getAIModel(),
        staleTime: 10 * 60 * 1000, // 10 minutes
    });
};

export const useTrainAIModel = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: () => apiService.trainAIModel(),
        onSuccess: () => {
            // Invalidate AI model and status queries
            queryClient.invalidateQueries({ queryKey: ['ai-model'] });
            queryClient.invalidateQueries({ queryKey: ['ai-status'] });
        },
    });
};

export const useAIStatus = () => {
    return useQuery({
        queryKey: ['ai-status'],
        queryFn: () => apiService.getAIStatus(),
        staleTime: 30 * 1000, // 30 seconds
        refetchInterval: 30 * 1000, // Refetch every 30 seconds
    });
}; 