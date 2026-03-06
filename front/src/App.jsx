import { useState } from 'react';
import { ChevronDown } from 'lucide-react'; // 아이콘 라이브러리 (필요시 설치)

const PerformancePage = () => {
  const [age, setAge] = useState('20대');
  const [gender, setGender] = useState('여자');
  const [isAgeOpen, setIsAgeOpen] = useState(false);
  const [isGenderOpen, setIsGenderOpen] = useState(false);

  // 샘플 데이터
  const items = [
    { id: 1, title: '호퍼스 뮤지컬 세트', desc: '역동적인 퍼포먼스와 감동의 무대 ❤️', price: '16,000원' },
    { id: 2, title: '우비핑구 연극 패키지', desc: '가족과 함께 즐기는 따뜻한 이야기', price: '15,000원' },
    { id: 3, title: '흰둥이 전시회 티켓', desc: '화이트초코처럼 달콤한 예술 세계 ✨', price: '8,500원' },
    { id: 4, title: '흰둥이 레저 체험권', desc: '귀여운 흰둥이와 함께하는 액티비티', price: '10,500원' },
  ];

  return (
    <div className="max-w-2xl mx-auto p-4 bg-white min-h-screen font-sans">
      {/* 🚀 상단 타이틀 (로고 스타일) */}
      <header className="py-6 mb-4">
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
          오늘의 공연/레저 🎭
        </h1>
      </header>

      {/* 📍 선택지 섹션 (드롭다운 2개) */}
      <div className="flex gap-4 mb-8 border-b pb-4">
        {/* 연령대 선택 */}
        <div className="relative">
          <button 
            onClick={() => {setIsAgeOpen(!isAgeOpen); setIsGenderOpen(false);}}
            className="flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-blue-600 transition"
          >
            {age} <ChevronDown size={16} />
          </button>
          {isAgeOpen && (
            <div className="absolute z-10 mt-2 w-32 bg-white border shadow-lg rounded-md overflow-hidden">
              {['10대', '20대', '30대', '40대', '50대'].map((v) => (
                <div 
                  key={v} 
                  className={`px-4 py-2 text-sm cursor-pointer hover:bg-blue-500 hover:text-white ${age === v ? 'bg-blue-600 text-white' : ''}`}
                  onClick={() => { setAge(v); setIsAgeOpen(false); }}
                >
                  {v}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 성별 선택 */}
        <div className="relative">
          <button 
            onClick={() => {setIsGenderOpen(!isGenderOpen); setIsAgeOpen(false);}}
            className="flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-blue-600 transition"
          >
            {gender} <ChevronDown size={16} />
          </button>
          {isGenderOpen && (
            <div className="absolute z-10 mt-2 w-32 bg-white border shadow-lg rounded-md overflow-hidden">
              {['남자', '여자'].map((v) => (
                <div 
                  key={v} 
                  className={`px-4 py-2 text-sm cursor-pointer hover:bg-blue-500 hover:text-white ${gender === v ? 'bg-blue-600 text-white' : ''}`}
                  onClick={() => { setGender(v); setIsGenderOpen(false); }}
                >
                  {v}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 📋 상품 리스트 그리드 (이미지 제외 버전) */}
      <div className="grid grid-cols-2 gap-x-4 gap-y-10">
        {items.map((item) => (
          <div key={item.id} className="flex flex-col relative group">
            {/* 이미지가 들어갈 자리를 심플한 박스로 대체 */}
            <div className="aspect-square bg-gray-50 rounded-xl mb-3 flex items-center justify-center border border-gray-100 group-hover:bg-gray-100 transition">
              <span className="bg-yellow-400 text-[10px] font-bold px-1.5 py-0.5 rounded absolute top-2 left-2">Best</span>
              <button className="absolute bottom-3 right-3 p-2 bg-white rounded-full shadow-md border border-gray-100 hover:scale-110 transition">
                🛒
              </button>
              <p className="text-gray-300 text-xs text-center px-4 leading-relaxed">
                상세 정보를 보려면 <br/> 클릭하세요
              </p>
            </div>

            {/* 텍스트 정보 */}
            <h3 className="text-base font-bold text-gray-800 mb-1">{item.title}</h3>
            <p className="text-sm text-gray-500 mb-3 leading-snug">{item.desc}</p>
            <span className="text-lg font-bold text-gray-900">{item.price}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PerformancePage;