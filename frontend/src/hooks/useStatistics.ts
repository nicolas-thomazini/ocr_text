import { useQuery } from '@tanstack/react-query';
import apiService from '../services/api';
import type { Statistics } from '../types';

export const useStatistics = () => {
    return useQuery({
        queryKey: ['statistics'],
        queryFn: () => apiService.getStatistics(),
        staleTime: 5 * 60 * 1000, // 5 minutes
        refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    });
}; 