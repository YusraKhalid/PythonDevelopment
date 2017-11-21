import axios from 'axios';
import { MYFACEBOOK_DOMAIN } from "../config"


export function RetrieveNews()
{
    const request = axios({
        method:'get',
        url: `${MYFACEBOOK_DOMAIN}news/`,
        headers: {'Authorization': `Token 9d7b79f8c45f6085a23732453dffeb6b4f240ae4`}
    });

    return {
        type: 'NEWS_LIST',
        payload: request
    };
}