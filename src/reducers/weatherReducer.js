
import * as types from '../actions/actionTypes';
import initialState from './initialState';
import _ from 'underscore'


export default function weatherReducer(state = initialState.weather, action) {
    switch(action.type) {
        case types.LOAD_WEATHER_REQUEST: {

            return{
                ...state,
                isFetching:true,message:'Loading...'
            }

        }
        case types.LOAD_WEATHER_SUCCESS: {

            return Object.assign({}, state, {
                series: state.series.map((item) => {
                        return Object.assign({}, item, {
                            data: item.data.concat(_.map(action.weather.list, (obj)=> {
                                    return {name: action.weather.city.name, y: obj.main[item.name]}
                                })
                            )
                        });
                }),
                xAxis:state.xAxis.map((axis) => {
                    return Object.assign({}, axis, {
                        categories:axis.categories.concat(_.pluck(action.weather.list,'dt_txt'))
                    });
                }),
                isFetching:action.weather.cod==='200'?false:true, message:action.weather.message
            })


        }
        case types.LOAD_WEATHER_FAILED: {
            return{
                ...state,
                isFetching:true,message:action.weather.message
            }

        }

        default:
            return state;
    }
}
