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
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PredictionChart = ({ predictions }) => {
  const data = {
    labels: predictions.map((_, index) => `House ${index + 1}`),
    datasets: [
      {
        label: 'Predicted Sale Price',
        data: predictions,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Sale Price Predictions Trend' },
    },
  };

  return <Line options={options} data={data} />;
};

export default PredictionChart;
