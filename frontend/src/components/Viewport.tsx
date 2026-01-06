import { Grid, OrbitControls } from '@react-three/drei'

/**
 * 3D Viewport component for structural model visualization.
 * Uses Three.js via React Three Fiber.
 */
function Viewport() {
  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />

      {/* Camera Controls */}
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        screenSpacePanning={false}
        maxPolarAngle={Math.PI / 2}
      />

      {/* Reference Grid */}
      <Grid
        args={[20, 20]}
        cellSize={1}
        cellThickness={0.5}
        cellColor="#404040"
        sectionSize={5}
        sectionThickness={1}
        sectionColor="#606060"
        fadeDistance={50}
        fadeStrength={1}
        followCamera={false}
        infiniteGrid={true}
      />

      {/* Axes Helper */}
      <axesHelper args={[5]} />

      {/* Origin Marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshStandardMaterial color="#ff4444" />
      </mesh>
    </>
  )
}

export default Viewport
