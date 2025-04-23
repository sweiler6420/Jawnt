import { axiosPrivate } from "../axios/axios"
import { useEffect } from "react"
import { useAppContext } from '../context/AppContext';
import { useNavigate } from 'react-router-dom'

export default function useAxiosPrivate() {
    const navigate = useNavigate()
    const { currentUser, currentOrganization, setCurrentUser, setCurrentOrganization } = useAppContext();

    useEffect(() => {
        if (!currentUser || !currentOrganization) return;
        
        const requestIntercept = axiosPrivate.interceptors.request.use(
            config => {

                config.headers['x-organization-id'] = currentOrganization.id;
                config.headers['x-employee-id'] = currentUser.id;
                
                return config
            }, (error) => Promise.reject(error)
        )

        const responseIntercept = axiosPrivate.interceptors.response.use(
            response => response,
            async (error) => {
                if(error?.response?.status === 403){
                    setCurrentUser(null);
                    setCurrentOrganization(null);
                    navigate('/login')
                }
                return Promise.reject(error)
            } 
        )

        return () => {
            axiosPrivate.interceptors.request.eject(requestIntercept)
            axiosPrivate.interceptors.response.eject(responseIntercept)
        }
    }, [currentUser, currentOrganization])

    return axiosPrivate
}