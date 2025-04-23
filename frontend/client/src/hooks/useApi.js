import axios from '../axios/axios'
import useAxiosPrivate from '../hooks/useAxiosPrivate'

export default function useApi() {
    const axiosPrivate = useAxiosPrivate()

    return {
        apiGet: apiGetFunction.bind(null, axiosPrivate),
        apiPost: apiPostFunction.bind(null, axiosPrivate),
        apiDelete: apiDeleteFunction.bind(null, axiosPrivate),
        apiPut: apiPutFunction.bind(null, axiosPrivate),
        apiLogin: apiLoginFunction.bind(null),
        apiCreateOrg: apiCreateOrgFunction.bind(null),
    }
}

export const apiCreateOrgFunction = async (endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axios.post(endpoint, params)
        return response.data
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}

export const apiLoginFunction = async (endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axios.post(endpoint, params)
        return response.data
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}


export const apiGetFunction = async (axiosPrivate, endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    const uriQuery = `?${URIEncodeObject(params)}`
    const url = `${endpoint}${uriQuery}`

    try{
        const response = await axiosPrivate.get(url)
        return {data: response.data}
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}


export const apiPostFunction = async (axiosPrivate, endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axiosPrivate.post(endpoint, _params)
        return {data: response.data}
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}


export const apiDeleteFunction = async (axiosPrivate, endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axiosPrivate.delete(endpoint, _params)
        return {data: response.data}
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}

export const apiPutFunction = async (axiosPrivate, endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axiosPrivate.put(endpoint, _params)
        return {data: response.data}
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}

function URIEncodeObject(o){
    return Object.entries(o)
        .map( ([key, val])=> encodeURIComponent(key) + '=' + encodeURIComponent(val) )
        .join('&')
}

function URIEncodeBody(body){
    return Object.keys(body).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(body[key])).join('&')
}