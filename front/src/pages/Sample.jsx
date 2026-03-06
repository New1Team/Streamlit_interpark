import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// 첫 번째 차트: 실시간 TOP10 예매율
const BarChart = ({ genreLabel, top10 }) => {
  const data = {
    labels: top10.map((item) => item.title),
    datasets: [
      {
        label: `${genreLabel} 실시간 TOP10 예매율`,
        data: top10.map((item) => item.bookingPercent),
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
      title: { display: true, text: '실시간 TOP10 예매율' },
    },
  };

  return <Bar data={data} options={options} />;
};

const Sample = () => {
  const genres = [
    { label: '레저/캠핑', value: 'LEISURE' },
    { label: '뮤지컬', value: 'MUSICAL' },
    { label: '콘서트', value: 'CONCERT' },
    { label: '연극', value: 'DRAMA' },
  ];

  const [selectedGenre, setSelectedGenre] = useState(genres[0]);

  const [summary, setSummary] = useState({
    totalCount: 0,
    avgBooking: 0,
  });

  const [top10, setTop10] = useState([]);

  const fetchRealtimeTop10 = async (genreValue) => {
    try {
      const res = await axios.get('http://192.168.0.105:8000/statistic/realtime-top10', {
        params: { genre: genreValue },
      });

      setSummary(res.data.summary || { totalCount: 0, avgBooking: 0 });
      setTop10(res.data.top10 || []);
    } catch (error) {
      console.error('실시간 TOP10 조회 실패:', error);
      setSummary({ totalCount: 0, avgBooking: 0 });
      setTop10([]);
    }
  };

  useEffect(() => {
    fetchRealtimeTop10(selectedGenre.value);
  }, [selectedGenre]);

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
            <span>{selectedGenre.label}</span>
            <span className="dropdown-toggle"></span>
          </button>
          <ul className="dropdown-menu w-100 shadow border-0">
            {genres.map((g) => (
              <li key={g.value}>
                <button className="dropdown-item" onClick={() => setSelectedGenre(g)}>
                  {g.label}
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
            <h3 className="fw-bold">{summary.totalCount}</h3>
          </div>
        </div>
        <div className="col-md-4">
          <div className="p-3 border rounded-3 bg-white shadow-sm">
            <p className="text-secondary small mb-1">평균 예매율</p>
            <h3 className="fw-bold">{summary.avgBooking}%</h3>
          </div>
        </div>
        <div className="col-md-4">
          <div className="p-3 border rounded-3 bg-white shadow-sm">
            <p className="text-secondary small mb-1">실시간 TOP10 수</p>
            <h3 className="fw-bold">{top10.length}</h3>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-12">
          <div className="p-4 shadow-sm border-0 bg-white rounded-4" style={{ height: '350px' }}>
            <BarChart genreLabel={selectedGenre.label} top10={top10} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sample;