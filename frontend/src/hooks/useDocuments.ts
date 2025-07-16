import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiService from '../services/api';

export const useDocuments = (page = 1, limit = 10) => {
    return useQuery({
        queryKey: ['documents', page, limit],
        queryFn: () => apiService.getDocuments(page, limit),
        staleTime: 5 * 60 * 1000, // 5 minutes
    });
};

export const useDocument = (id: string) => {
    return useQuery({
        queryKey: ['document', id],
        queryFn: () => apiService.getDocument(id),
        enabled: !!id,
        staleTime: 5 * 60 * 1000,
    });
};

export const useUploadDocument = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ file, description }: { file: File; description?: string }) =>
            apiService.uploadDocument(file, description),
        onSuccess: () => {
            // Invalidate and refetch documents
            queryClient.invalidateQueries({ queryKey: ['documents'] });
        },
    });
};

export const useDeleteDocument = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => apiService.deleteDocument(id),
        onSuccess: () => {
            // Invalidate and refetch documents
            queryClient.invalidateQueries({ queryKey: ['documents'] });
        },
    });
};

export const useProcessDocument = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (id: string) => apiService.processDocument(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['documents'] });
        },
    });
}; 