import axios from 'axios';

export const GET_WEATHER = 'GET_WEATHER';
const BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast?appid=198c6e1e72c287674ae7d1888c8f9cff';

export function  getWeather(cityName) {

    const weatherFetchUrl = `${BASE_URL}&q=${cityName},us`;
    return({
            type: GET_WEATHER,
            payload: axios.get(weatherFetchUrl)
        }
    )
}
