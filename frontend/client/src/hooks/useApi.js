import axios from '../axios/axios'

export default function useApi() {

    return {
        apiGet: apiGetFunction.bind(null),
        apiPost: apiPostFunction.bind(null),
        // apiDelete: apiCall.bind(null, 'delete'),
        // apiPut: apiCall.bind(null, 'put'),
    }
}


export const apiGetFunction = async (endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    const uriQuery = `?${URIEncodeObject(params)}`
    const url = `${endpoint}${uriQuery}`

    try{
        const response = await axios.get(url)
        return {data: response.data}
    } catch (err) {
        console.log(err)
        return {"status": err.request.status, "message": err.message, "error": err.name}
    }

}


export const apiPostFunction = async (endpoint, _params={})=> {
    const {rawResponse=false, ...params} = _params

    try{
        const response = await axios.post(endpoint, _params)
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