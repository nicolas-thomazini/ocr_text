import { useQuery } from '@tanstack/react-query';
import apiService from '../services/api';

export const useStatistics = () => {
    return useQuery({
        queryKey: ['statistics'],
        queryFn: () => apiService.getStatistics(),
        staleTime: 5 * 60 * 1000, // 5 minutes
        refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    });
}; 