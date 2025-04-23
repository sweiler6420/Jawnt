import React, { useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import useApi from '../hooks/useApi'; // Assuming you're using the useApi hook

const AppInitializer = () => {
    const { currentUser, currentOrganization, setCurrentInternalAccount, setCurrentExternalAccount, setCurrentDebitCard, setCurrentIdempotencyKey,
        currentInternalAccount, currentExternalAccount, currentDebitCard, currentIdempotencyKey} = useAppContext();
    const { apiGet } = useApi(); // Your custom API hook

    useEffect(() => {
        const fetchEmployeeData = async () => {
            // Check if the data has already been fetched (avoid re-fetching)
            if (currentInternalAccount && currentExternalAccount && currentDebitCard && currentIdempotencyKey) {
                return; // If all the account data is already set, don't fetch again
            }

            try {
                const response = await apiGet('/employee');
                setCurrentInternalAccount(response.data.internal_account)
                setCurrentExternalAccount(response.data.external_account)
                setCurrentDebitCard(response.data.debit_card)
                setCurrentIdempotencyKey(response.data.idempotency_key)
            } catch (err) {
                console.error('Failed to fetch employee data', err);
            }
        };

        // Trigger data fetching if both currentUser and currentOrganization are set
        if (currentUser?.id && currentOrganization?.id) {
            fetchEmployeeData();
        }
    }, [currentUser?.id, currentOrganization?.id, apiGet]);

  return null; // This component doesn't render anything directly
};

export default AppInitializer;
