
import React from 'react';

function Forecast({ city, openWeatherData, weatherApiData }) {
  if (!openWeatherData || !weatherApiData) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      {/*current */}
      <section className="mb-8">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">{city.toUpperCase()}</h2>
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Condizioni Attuali</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 border rounded-lg">
            <h3 className="text-xl font-semibold text-gray-700 mb-3">OpenWeather</h3>
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-800">{openWeatherData.current.temp}°C</div>
              <div className="text-gray-600">{openWeatherData.current.condition}</div>
            </div>
          </div>

          <div className="p-4 border rounded-lg">
            <h3 className="text-xl font-semibold text-gray-700 mb-3">WeatherAPI</h3>
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-800">{weatherApiData.current.temp}°C</div>
              <div className="text-gray-600">{weatherApiData.current.condition}</div>
            </div>
          </div>
        </div>
      </section>

      {/* hourly */}
      <section className="mb-8">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Previsioni Orarie</h2>
        
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-700 mb-3">OpenWeather</h3>
          <div className="flex overflow-x-auto gap-4 pb-4">
            {openWeatherData.hourly.map((hour, index) => (
              <div key={index} className="flex-shrink-0 p-4 border rounded-lg bg-gray-50 min-w-[140px]">
                <h4 className="font-semibold text-gray-700">{hour.time}</h4>
                <div className="text-2xl font-bold text-gray-800">{hour.temp}°C</div>
                <div className="text-gray-600">{hour.condition}</div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-3">WeatherAPI</h3>
          <div className="flex overflow-x-auto gap-4 pb-4">
            {weatherApiData.hourly.map((hour, index) => (
              <div key={index} className="flex-shrink-0 p-4 border rounded-lg bg-gray-50 min-w-[140px]">
                <h4 className="font-semibold text-gray-700">{hour.time}</h4>
                <div className="text-2xl font-bold text-gray-800">{hour.temp}°C</div>
                <div className="text-gray-600">{hour.condition}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* daily*/}
      <section>
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Previsioni Giornaliere</h2>
        
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-700 mb-3">OpenWeather</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {Object.entries(openWeatherData.daily).map(([date, data], index) => (
              <div key={index} className="p-4 border rounded-lg bg-gray-50">
                <h4 className="font-semibold text-gray-700">{date}</h4>
                <div className="my-2">
                  <div className="text-orange-600 font-bold">Max: {Math.max(...data.temps)}°C</div>
                  <div className="text-blue-600 font-bold">Min: {Math.min(...data.temps)}°C</div>
                </div>
                <div className="text-gray-600">{data.conditions[Math.floor(data.conditions.length / 2)]}</div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-3">WeatherAPI</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {weatherApiData.daily.map((day, index) => (
              <div key={index} className="p-4 border rounded-lg bg-gray-50">
                <h4 className="font-semibold text-gray-700">{day.date}</h4>
                <div className="my-2">
                  <div className="text-orange-600 font-bold">Max: {day.maxTemp}°C</div>
                  <div className="text-blue-600 font-bold">Min: {day.minTemp}°C</div>
                </div>
                <div className="text-gray-600">{day.condition}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default Forecast;