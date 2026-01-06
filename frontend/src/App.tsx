import { Canvas } from '@react-three/fiber'
import Viewport from './components/Viewport'

function App() {
  return (
    <div className="h-screen w-screen flex flex-col bg-gray-900">
      {/* Header */}
      <header className="h-12 bg-gray-800 border-b border-gray-700 flex items-center px-4">
        <h1 className="text-white font-bold text-lg">PAZ</h1>
        <span className="text-gray-400 text-sm ml-2">v1.0.0-mvp</span>
        <div className="ml-auto flex gap-2">
          <button className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
            Nuevo Proyecto
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Sidebar - Model Tree */}
        <aside className="w-64 bg-gray-800 border-r border-gray-700 p-4">
          <h2 className="text-white font-semibold mb-4">Modelo</h2>
          <div className="text-gray-400 text-sm">
            <p>Nodos: 0</p>
            <p>Frames: 0</p>
            <p>Materiales: 0</p>
            <p>Secciones: 0</p>
          </div>
        </aside>

        {/* 3D Viewport */}
        <main className="flex-1">
          <Canvas
            camera={{ position: [10, 10, 10], fov: 50 }}
            className="bg-gray-950"
          >
            <Viewport />
          </Canvas>
        </main>

        {/* Properties Panel */}
        <aside className="w-72 bg-gray-800 border-l border-gray-700 p-4">
          <h2 className="text-white font-semibold mb-4">Propiedades</h2>
          <p className="text-gray-400 text-sm">
            Selecciona un elemento para ver sus propiedades
          </p>
        </aside>
      </div>

      {/* Status Bar */}
      <footer className="h-6 bg-gray-800 border-t border-gray-700 flex items-center px-4 text-xs text-gray-400">
        <span>Listo</span>
        <span className="ml-auto">Sistema de unidades: m / kN</span>
      </footer>
    </div>
  )
}

export default App
