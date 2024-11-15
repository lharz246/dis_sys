// src/components/Forecast.js
import React from 'react';
import './Forecast.css';

function Forecast({ currentWeather, hourlyForecast, dailyForecast }) {
  if (!currentWeather) return null;

  return (
    <div className="forecast">
      {/* current */}
      <section className="current-weather">
        <h2>{currentWeather.city} - Condizioni Attuali</h2>
        <div className="weather-info">
          <div className="weather-card">
            <h3>Temperatura</h3>
            <div className="sources">
              <small>OpenWeather: {currentWeather.temperature.openweather}°C</small>
              <small>WeatherAPI: {currentWeather.temperature.weatherapi}°C</small>
            </div>
          </div>
          <div className="weather-card">
            <h3>Condizioni</h3>
            <div className="conditions">
              <div>OpenWeather: {currentWeather.condition.openweather}</div>
              <div>WeatherAPI: {currentWeather.condition.weatherapi}</div>
            </div>
          </div>
        </div>
      </section>

      {/* hourly*/}
      {hourlyForecast && (
        <section className="hourly-forecast">
          <h2>Previsioni Orarie</h2>
          <div className="forecast-scroll">
            {hourlyForecast.map((hour, index) => (
              <div key={index} className="forecast-card">
                <h3>{hour.time}</h3>
                <div className="forecast-sources">
                  <div className="source">
                    <h4>OpenWeather</h4>
                    <div className="temp">{hour.openweather.temp}°C</div>
                    <div className="condition">{hour.openweather.condition}</div>
                  </div>
                  <div className="source">
                    <h4>WeatherAPI</h4>
                    <div className="temp">{hour.weatherapi.temp}°C</div>
                    <div className="condition">{hour.weatherapi.condition}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/*5 days*/}
      {dailyForecast && (
        <section className="daily-forecast">
          <h2>Next 5 Days</h2>
          <div className="forecast-grid">
            {dailyForecast.map((day, index) => (
              <div key={index} className="forecast-card">
                <h3>{day.date}</h3>
                <div className="forecast-sources">
                  <div className="source">
                    <h4>OpenWeather</h4>
                    <div className="temp-range">
                      <div className="max">Max: {day.openweather.maxTemp}°C</div>
                      <div className="min">Min: {day.openweather.minTemp}°C</div>
                    </div>
                    <div className="condition">{day.openweather.condition}</div>
                  </div>
                  <div className="source">
                    <h4>WeatherAPI</h4>
                    <div className="temp-range">
                      <div className="max">Max: {day.weatherapi.maxTemp}°C</div>
                      <div className="min">Min: {day.weatherapi.minTemp}°C</div>
                    </div>
                    <div className="condition">{day.weatherapi.condition}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default Forecast;