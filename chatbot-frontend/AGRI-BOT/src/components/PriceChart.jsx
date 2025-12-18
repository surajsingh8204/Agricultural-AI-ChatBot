import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PriceChart = ({ dailyForecast, crop, state, trend }) => {
  if (!dailyForecast || dailyForecast.length === 0) {
    return null;
  }

  // Prepare data for chart
  const labels = dailyForecast.map(day => {
    const date = new Date(day.date);
    return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
  });

  const prices = dailyForecast.map(day => day.price);

  // Determine color based on trend
  const isUpward = trend?.toLowerCase().includes('up') || trend?.toLowerCase().includes('rising');
  const isDownward = trend?.toLowerCase().includes('down') || trend?.toLowerCase().includes('falling');
  
  let lineColor, backgroundColor;
  if (isUpward) {
    lineColor = 'rgb(34, 197, 94)';  // Green
    backgroundColor = 'rgba(34, 197, 94, 0.1)';
  } else if (isDownward) {
    lineColor = 'rgb(239, 68, 68)';  // Red
    backgroundColor = 'rgba(239, 68, 68, 0.1)';
  } else {
    lineColor = 'rgb(59, 130, 246)';  // Blue (stable)
    backgroundColor = 'rgba(59, 130, 246, 0.1)';
  }

  const data = {
    labels,
    datasets: [
      {
        label: `${crop} Price (₹/quintal)`,
        data: prices,
        borderColor: lineColor,
        backgroundColor: backgroundColor,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: lineColor,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: `${crop} Price Forecast - ${state}`,
        color: '#e5e7eb',
        font: {
          size: 14,
          weight: '600',
        },
        padding: {
          bottom: 10
        }
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#fff',
        bodyColor: '#e5e7eb',
        borderColor: lineColor,
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        displayColors: false,
        callbacks: {
          label: function(context) {
            return `₹${context.parsed.y.toFixed(2)}/quintal`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(75, 85, 99, 0.3)',
        },
        ticks: {
          color: '#9ca3af',
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(75, 85, 99, 0.3)',
        },
        ticks: {
          color: '#9ca3af',
          font: {
            size: 11
          },
          callback: function(value) {
            return '₹' + value.toFixed(0);
          }
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
  };

  return (
    <div className="price-chart-container">
      <div className="chart-wrapper">
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default PriceChart;
