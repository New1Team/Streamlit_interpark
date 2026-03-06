import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';


ChartJS.register(CategoryScale, LinearScale, BarElement,PointElement,
  LineElement, Title, Tooltip, Legend);

// 첫 번째 차트: 연령대별 예매율
const BarChart = ({ genre }) => {
  const data = {
    labels: ['10대', '20대', '30대', '40대', '50대', '60대'],
    datasets: [
      {
        label: `${genre} 연령대별 예매율`,
        data: [46, 28, 7, 6, 5, 4],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: '연령대별 예매 현황' },
    },
  };

  return <Bar data={data} options={options} />;}; 


const LineChart = ({ genre }) => {
  const data = {
    labels: ['1위', '2위', '3위', '4위', '5위'],
    datasets: [
      {
        label: `${genre} 할인율`,
        data: [50, 40, 30, 20, 10],
        backgroundColor: 'rgb(50, 54, 168)',
        borderColor: 'rgb(50, 54, 168)',
        borderWidth: 1,
        tension : 0.3
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: '장르별 할인율 순위' },
    },
  };

 
  return <Line data={data} options={options} />;
};

const Sample = () => {
  const [selectedGenre, setSelectedGenre] = useState('레저/캠핑');
  const genres = ['레저/캠핑', '뮤지컬', '콘서트', '연극'];

  return (
    <div className="container py-5" style={{ maxWidth: '1000px' }}>
      <h2 className="fw-bold mb-4">인터파크 공연 분석 대시보드</h2>

      {/* 장르 선택 박스 */}
      <div className="mb-4 text-start">
        <label className="form-label small text-secondary">장르 선택</label>
        <div className="dropdown">
          <button
            className="btn w-100 d-flex justify-content-between align-items-center p-3 shadow-sm border-0 bg-light"
            type="button"
            data-bs-toggle="dropdown"
          >
            <span>{selectedGenre}</span>
            <span className="dropdown-toggle"></span>
          </button>
          <ul className="dropdown-menu w-100 shadow border-0">
            {genres.map((g) => (
              <li key={g}>
                <button className="dropdown-item" onClick={() => setSelectedGenre(g)}>
                  {g}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* 통계 수치 섹션 */}
      <div className="row g-4 mb-5 text-center">
        <div className="col-md-4">
          <div className="p-3 border rounded-3 bg-white shadow-sm">
            <p className="text-secondary small mb-1">공연 수</p>
            <h3 className="fw-bold">43</h3>
          </div>
        </div>
        <div className="col-md-4">
          <div className="p-3 border rounded-3 bg-white shadow-sm">
            <p className="text-secondary small mb-1">평균 예매율</p>
            <h3 className="fw-bold">2.3%</h3>
          </div>
        </div>
        <div className="col-md-4">
          <div className="p-3 border rounded-3 bg-white shadow-sm">
            <p className="text-secondary small mb-1">7일 이내 마감 공연 수</p>
            <h3 className="fw-bold">0</h3>
          </div>
        </div>
      </div>

      
      <div className="row g-4">
        <div className="col12">
          <div className="p-4 shadow-sm border-0 bg-white rounded-4" style={{ height: '350px' }}>
            <BarChart genre={selectedGenre} />
          </div>
        </div>
        <div className="col12">
          <div className="p-4 shadow-sm border-0 bg-white rounded-4" style={{ height: '350px' }}>
            <LineChart genre={selectedGenre} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sample;