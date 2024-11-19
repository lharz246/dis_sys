import React from 'react';
import axios from 'axios';
import SearchBox from './components/SearchBox';
import Forecast from './components/Forecast';
import './App.css';

const openweathermapKey = 'adba1b8838389cf7c4399cdecf7982f2'
const weatherapicomKey = 'd91aaaf5dd224d86a27160734241511'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      city: '',
      openWeatherData: null,
      weatherApiData: null
    };
  }

  fetchWeatherData = async (city) => {
    try {
      //api
      const [openWeatherCurrent, openWeatherForecast, weatherApiResponse] = await Promise.all([
        axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${openweathermapKey}`),
        axios.get(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&units=metric&appid=${openweathermapKey}`),
        axios.get(`https://api.weatherapi.com/v1/forecast.json?key=${weatherapicomKey}&q=${city}&days=5&aqi=no`)
        
      ]);

      //OpenWeather
      const openWeatherData = {
        current: {
          temp: openWeatherCurrent.data.main.temp,
          condition: openWeatherCurrent.data.weather[0].main
        },
        hourly: openWeatherForecast.data.list.slice(0, 6).map(item => ({
          time: new Date(item.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          temp: item.main.temp,
          condition: item.weather[0].main
        })),
        daily: openWeatherForecast.data.list.reduce((acc, item) => {
          const date = new Date(item.dt * 1000).toLocaleDateString();
          if (!acc[date]) {
            acc[date] = {
              temps: [],
              conditions: []
            };
          }
          acc[date].temps.push(item.main.temp);
          acc[date].conditions.push(item.weather[0].main);
          return acc;
        }, {})
      };

      //WeatherAPI
      const weatherApiData = {
        current: {
          temp: weatherApiResponse.data.current.temp_c,
          condition: weatherApiResponse.data.current.condition.text
        },
        hourly: weatherApiResponse.data.forecast.forecastday[0].hour
          .filter((_, index) => index % 3 === 0)
          .slice(0, 6)
          .map(hour => ({
            time: new Date(hour.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            temp: hour.temp_c,
            condition: hour.condition.text
          })),
        daily: weatherApiResponse.data.forecast.forecastday.map(day => ({
          date: new Date(day.date).toLocaleDateString(),
          maxTemp: day.day.maxtemp_c,
          minTemp: day.day.mintemp_c,
          condition: day.day.condition.text
        }))
      };

      this.setState({
        city,
        openWeatherData,
        weatherApiData
      });

    } catch (error) {
      console.error('Errore nel recupero dei dati meteo:', error);
      alert('Errore nel recupero dei dati meteo. Controlla la console per i dettagli.');
    }
  };

  render() {
    const { city, openWeatherData, weatherApiData } = this.state;
    
    return (
      <div className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-6">
          Weather Mashup
        </h1>
        <div className="max-w-3xl mx-auto mb-6">
          <SearchBox onSearch={this.fetchWeatherData} />
        </div>
        <Forecast 
          city={city}
          openWeatherData={openWeatherData}
          weatherApiData={weatherApiData}
        />
      </div>
    );
  }
}

export default App;