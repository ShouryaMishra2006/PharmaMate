import PrescriptionScanner from './components/PrescriptionScanner.jsx';
function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-3xl text-center">
        
        <div className="space-y-6">
          <PrescriptionScanner/>
          <div className="border-t border-gray-300"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
