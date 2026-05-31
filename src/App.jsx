import React, { useState, useEffect } from 'react';
import { Stethoscope, Building2, TrendingUp, Info, BarChart3, Users } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LabelList, Cell } from 'recharts';

export default function App() {
  const [db, setDb] = useState(null);
  const [loading, setLoading] = useState(true);
  const [modalItem, setModalItem] = useState(null);

  const openModal = (item) => setModalItem(item);
  const closeModal = () => setModalItem(null);

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16', '#f43f5e', '#14b8a6'];

  useEffect(() => {
    fetch('/data.json')
      .then(res => res.json())
      .then(data => { setDb(data); setLoading(false); })
      .catch(err => setLoading(false));
  }, []);

  if (loading || !db) return <div className="min-h-screen bg-slate-100 flex items-center justify-center text-blue-800 font-bold text-xl">กำลังเตรียมข้อมูล Dashboard...</div>;

  return (
    <div className="min-h-screen bg-[#f3f4f6] text-slate-900 font-sans">
      
      {/* 1. Dark Corporate Navbar */}
      <nav className="bg-[#1e293b] text-white px-6 py-4 flex flex-col md:flex-row justify-between items-start md:items-center shadow-md z-50 relative w-full">
        <div className="flex items-center gap-4">
          
          {/* ปรับโลโก้ให้ขนาดพอดีสายตา */}
          <div className="bg-white p-1.5 rounded-full shadow-md flex items-center justify-center w-14 h-14 overflow-hidden border-2 border-slate-700">
            <img 
              src="/logo.png" 
              alt="Logo" 
              className="w-full h-full object-contain"
              onError={(e) => { e.target.style.display = 'none'; }}
            />
          </div>
          
          <div>
            <h1 className="text-xl md:text-2xl font-bold tracking-tight text-white">Dashboard ข้อมูลกองทุนแพทย์แผนไทย</h1>
            <div className="flex items-center gap-3 mt-1">
              <p className="text-[13px] text-slate-300">ภาพรวม สำนักงานสาธารณสุขอำเภออรัญประเทศ</p>
              <span className="bg-slate-700 px-2 py-0.5 rounded text-[11px] font-bold text-slate-200 border border-slate-600">ปีงบ 2569</span>
            </div>
          </div>
        </div>
      </nav>

      {/* แถบอ้างอิงที่มาข้อมูล NHSO */}
      <div className="bg-blue-50 border-b border-blue-100 px-6 py-2.5 flex flex-col md:flex-row justify-between items-center text-[13px] shadow-sm w-full">
        <div className="text-blue-800 font-bold flex items-center gap-2">
          <Info size={16} />
          อ้างอิงข้อมูลจากระบบ สปสช. (NHSO): 
          <a href="https://medata.nhso.go.th/dashboard.viz?ref=wEJcuu5y" target="_blank" rel="noreferrer" className="underline hover:text-blue-600 transition-colors">
            https://medata.nhso.go.th/dashboard.viz?ref=wEJcuu5y
          </a>
        </div>
        <div className="text-slate-600 font-bold mt-2 md:mt-0">
          ข้อมูลอัปเดตล่าสุด: {new Date().toLocaleDateString('th-TH')}
        </div>
      </div>

      {/* Main Container */}
      <div className="p-4 md:p-6 lg:p-8 w-full mx-auto space-y-6">
        
        {/* KPI Summary Cards - ปรับความสูงและตัวเลขให้พอดี */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
          <div className="bg-white p-6 rounded-2xl border-l-[6px] border-[#22c55e] shadow-sm relative overflow-hidden flex flex-col justify-center h-[120px]">
            <p className="text-slate-600 text-[12px] font-bold mb-2">ประมาณการยอดเงินที่จะได้รับจริง</p>
            <h3 className="text-3xl md:text-4xl font-black text-[#22c55e] tracking-tight leading-none">฿{db.overview.total_amount.toLocaleString()}</h3>
          </div>
          
          <div className="bg-white p-6 rounded-2xl border-l-[6px] border-[#3b82f6] shadow-sm relative overflow-hidden flex flex-col justify-center h-[120px]">
            <p className="text-slate-600 text-[12px] font-bold mb-2">POINT</p>
            <h3 className="text-3xl md:text-4xl font-black text-[#1e293b] tracking-tight leading-none">{db.overview.total_points.toLocaleString()}</h3>
            <BarChart3 className="absolute right-[-15px] bottom-[-15px] text-slate-50 w-28 h-28 rotate-12 pointer-events-none" />
          </div>
          
          <div className="bg-white p-6 rounded-2xl border-l-[6px] border-[#f59e0b] shadow-sm relative overflow-hidden flex flex-col justify-center h-[120px]">
            <p className="text-slate-600 text-[12px] font-bold mb-2">หน่วยบริการในเครือข่ายทั้งหมด</p>
            <h3 className="text-3xl md:text-4xl font-black text-[#1e293b] tracking-tight leading-none">16</h3>
            <Users className="absolute right-[-15px] bottom-[-15px] text-slate-50 w-28 h-28 rotate-12 pointer-events-none" />
          </div>
        </section>

        {/* Data View (Chart & Table) */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full">
          
          {/* กราฟแท่ง */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 w-full flex flex-col">
            <h3 className="text-[15px] font-bold text-slate-800 mb-6 flex items-center gap-2 border-b pb-3">
              <TrendingUp className="text-blue-600" size={18}/> บริการแพทย์แผนไทย นวด อบ ประคบ
            </h3>
            
            <div className="w-full h-[350px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={db.hospitals} margin={{ top: 10, right: 10, left: 0, bottom: 60 }}>
                  <defs>
                    <linearGradient id="colorPoints" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={1}/>
                      <stop offset="95%" stopColor="#1d4ed8" stopOpacity={0.8}/>
                    </linearGradient>
                    <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={1}/>
                      <stop offset="95%" stopColor="#047857" stopOpacity={0.8}/>
                    </linearGradient>
                  </defs>

                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  {/* ลดขนาดฟอนต์แกนกราฟ */}
                  <XAxis dataKey="name" tick={{ fill: '#475569', fontSize: 11, fontWeight: 'bold' }} axisLine={false} tickLine={false} angle={-45} textAnchor="end" />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} width={60} />
                  <Tooltip 
                    cursor={{fill: '#f8fafc'}} 
                    contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', fontSize: '12px' }}
                  />
                  <Bar dataKey="points" name="POINT" fill="url(#colorPoints)" radius={[4, 4, 0, 0]} barSize={20} />
                  <Bar dataKey="amount" name="ประมาณการยอดเงิน" fill="url(#colorAmount)" radius={[4, 4, 0, 0]} barSize={20} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100">
               <img 
                 src="/med.png" 
                 alt="Medical Banner" 
                 className="w-full h-auto rounded-lg shadow-sm"
                 onError={(e) => { e.target.style.display = 'none'; }}
               />
            </div>
          </div>

          {/* ตารางข้อมูล */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full w-full">
            <div className="p-6 border-b border-slate-200 flex justify-between items-center bg-white">
              <h3 className="text-[15px] font-bold text-slate-800 flex items-center gap-2">
                <Info className="text-blue-600" size={18}/> สรุปประสิทธิภาพการเบิกจ่าย แยกรายสถานพยาบาล
              </h3>
              <span className="text-emerald-700 font-bold text-[11px] bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 shadow-sm">
                ประมาณการ 1 บาท/Point
              </span>
            </div>

            <div className="overflow-x-auto flex-1 h-[350px]">
              <table className="w-full text-left whitespace-nowrap">
                <thead className="bg-[#f8fafc] sticky top-0 z-10 shadow-sm">
                  {/* ลดขนาดหัวตาราง */}
                  <tr className="text-slate-500 font-bold text-[11px] uppercase tracking-wider">
                    <th className="py-3 px-4 border-b border-slate-200 w-12 text-center">อันดับ</th>
                    <th className="py-3 px-4 border-b border-slate-200">หน่วยบริการ</th>
                    <th className="py-3 px-4 text-right border-b border-slate-200">POINT</th>
                    <th className="py-3 px-4 text-right border-b border-slate-200 pr-6">ประมาณการยอดเงิน</th>
                  </tr>
                </thead>
                {/* ลดขนาดเนื้อหาในตาราง */}
                <tbody className="divide-y divide-slate-100 text-[13px]">
                  {db.hospitals.map((item, index) => (
                    <tr key={item.name} onClick={() => openModal(item)} className="cursor-pointer hover:bg-slate-50 transition-colors group">
                      <td className="py-3 px-4 text-slate-500 font-medium text-center">{index + 1}</td>
                      <td className="py-3 px-4 font-bold text-slate-800 group-hover:text-blue-600 transition-colors">{item.name}</td>
                      <td className="py-3 px-4 text-right font-bold text-slate-600">{item.points.toLocaleString()}</td>
                      <td className="py-3 px-4 text-right font-bold text-blue-700 pr-6">{item.amount.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>

      {/* 4. Pop-up ขนาดใหญ่ */}
      {modalItem && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8 bg-slate-900/70 backdrop-blur-sm" onClick={closeModal}>
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl p-6 md:p-8 border-t-[6px] border-[#1e3a8a] animate-in zoom-in-95 duration-200" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-6 border-b pb-4">
              <h4 className="font-bold text-xl text-slate-900 tracking-tight flex items-center gap-2">
                <Stethoscope className="text-blue-700" size={24} /> 
                {modalItem.name}
              </h4>
              <button onClick={closeModal} className="text-slate-500 hover:text-red-600 hover:bg-red-50 p-2 rounded-full transition-colors text-xl">✕</button>
            </div>
            
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={modalItem.services} layout="vertical" margin={{ left: 10, right: 50, top: 10, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={true} vertical={false} />
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" width={180} tick={{fontSize: 12, fontWeight: 'bold', fill: '#334155'}} axisLine={false} tickLine={false} />
                  
                  <Tooltip 
                    cursor={{fill: '#f8fafc'}}
                    contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', padding: '8px 12px', fontSize: '12px', fontWeight: 'bold' }}
                  />
                  
                  <Bar dataKey="points" name="จำนวน Point" barSize={24} radius={[0, 4, 4, 0]}>
                    {modalItem.services.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                    <LabelList dataKey="points" position="right" formatter={v => v.toLocaleString()} fontSize={12} fontWeight="bold" fill="#0f172a" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}