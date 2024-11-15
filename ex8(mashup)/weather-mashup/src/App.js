
import React from 'react';
import axios from 'axios';
import SearchBox from './components/SearchBox';
import Forecast from './components/Forecast';
import './App.css';

const openweathermapObj = {
  key: 'adba1b8838389cf7c4399cdecf7982f2',
  base: 'https://api.openweathermap.org/data/2.5'
};

const weatherapicomObj = {
  key: 'd91aaaf5dd224d86a27160734241511',
  base: 'https://api.weatherapi.com/v1'
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentWeather: null,
      hourlyForecast: null,
      dailyForecast: null
    };
  }

  fetchWeatherData = async (city) => {
    try {
      const [openWeatherCurrent, openWeatherForecast, weatherApiResponse] = await Promise.all([
        axios.get(`${openweathermapObj.base}/weather?q=${city}&units=metric&appid=${openweathermapObj.key}`),
        axios.get(`${openweathermapObj.base}/forecast?q=${city}&units=metric&appid=${openweathermapObj.key}`),
        axios.get(`${weatherapicomObj.base}/forecast.json?key=${weatherapicomObj.key}&q=${city}&days=5&aqi=no`)
      ]);

      //current
      const currentWeather = {
        city: city,
        temperature: {
          openweather: openWeatherCurrent.data.main.temp,
          weatherapi: weatherApiResponse.data.current.temp_c,
        },
        condition: {
          openweather: openWeatherCurrent.data.weather[0].main,
          weatherapi: weatherApiResponse.data.current.condition.text
        }
      };

      const hourlyForecast = openWeatherForecast.data.list
        .slice(0, 6)  //first 6 3 hour intervals
        .map((item, index) => ({
          time: new Date(item.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          openweather: {
            temp: item.main.temp,
            condition: item.weather[0].main
          },
          weatherapi: {
            temp: weatherApiResponse.data.forecast.forecastday[0].hour[index * 3].temp_c,
            condition: weatherApiResponse.data.forecast.forecastday[0].hour[index * 3].condition.text
          }
        }));

      // daily
      const dailyForecast = [];
      
      //openweather daily
      const openWeatherDaily = {};
      openWeatherForecast.data.list.forEach(item => {
        const date = new Date(item.dt * 1000).toLocaleDateString();
        if (!openWeatherDaily[date]) {
          openWeatherDaily[date] = {
            temps: [],
            conditions: []
          };
        }
        openWeatherDaily[date].temps.push(item.main.temp);
        openWeatherDaily[date].conditions.push(item.weather[0].main);
      });

      // Combina i dati delle due API
      weatherApiResponse.data.forecast.forecastday.forEach((day, index) => {
        const date = new Date(day.date).toLocaleDateString();
        const openWeatherData = openWeatherDaily[date] || { temps: [], conditions: [] };
        
        dailyForecast.push({
          date: date,
          openweather: {
            maxTemp: Math.max(...openWeatherData.temps),
            minTemp: Math.min(...openWeatherData.temps),
            condition: openWeatherData.conditions[Math.floor(openWeatherData.conditions.length / 2)] 
          },
          weatherapi: {
            maxTemp: day.day.maxtemp_c,
            minTemp: day.day.mintemp_c,
            condition: day.day.condition.text
          }
        });
      });

      this.setState({
        currentWeather,
        hourlyForecast,
        dailyForecast
      });

    } catch (error) {
      console.error('Errore nel recupero dei dati meteo:', error);
      alert('Errore nel recupero dei dati meteo. Controlla la console per i dettagli.');
    }
  };

  render() {
    const { currentWeather, hourlyForecast, dailyForecast } = this.state;
    
    return (
      <div className="app">
        <h1>Weather Mashup</h1>
        <SearchBox onSearch={this.fetchWeatherData} />
        <Forecast 
          currentWeather={currentWeather}
          hourlyForecast={hourlyForecast}
          dailyForecast={dailyForecast}
        />
      </div>
    );
  }
}

export default App;