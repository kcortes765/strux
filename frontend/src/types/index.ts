/**
 * Shared TypeScript types for PAZ Frontend.
 */

// Unit System
export type LengthUnit = 'm' | 'cm' | 'mm' | 'ft' | 'in'
export type ForceUnit = 'kN' | 'N' | 'kgf' | 'ton' | 'kip' | 'lb'
export type AngleUnit = 'deg' | 'rad'

export interface UnitSystem {
  length: LengthUnit
  force: ForceUnit
  angle: AngleUnit
}

// Coordinates
export interface Point3D {
  x: number
  y: number
  z: number
}

// Restraints (boundary conditions)
export interface Restraint {
  ux: boolean  // Translation X
  uy: boolean  // Translation Y
  uz: boolean  // Translation Z
  rx: boolean  // Rotation X
  ry: boolean  // Rotation Y
  rz: boolean  // Rotation Z
}

// Node
export interface Node extends Point3D {
  id: number
  restraint: Restraint
}

// Frame Element
export interface Frame {
  id: number
  nodeI: number
  nodeJ: number
  materialId: string
  sectionId: string
  rotation: number
  releases?: FrameReleases
}

// Frame End Releases
export interface FrameReleases {
  startI: Restraint
  endJ: Restraint
}

// Material Types
export type MaterialType = 'steel' | 'concrete' | 'timber' | 'aluminum' | 'custom'

export interface Material {
  id: string
  name: string
  type: MaterialType
  E: number    // Elastic modulus (Pa)
  G: number    // Shear modulus (Pa)
  nu: number   // Poisson's ratio
  rho: number  // Density (kg/m³)
  fy?: number  // Yield strength (Pa)
  fu?: number  // Ultimate strength (Pa)
  fc?: number  // Compressive strength (Pa) - for concrete
}

// Section Types
export type SectionType = 'W' | 'HSS' | 'L' | 'C' | 'T' | 'Pipe' | 'Rectangular' | 'Circular' | 'Custom'

export interface Section {
  id: string
  name: string
  type: SectionType
  A: number    // Area (m²)
  Ix: number   // Moment of inertia X (m⁴)
  Iy: number   // Moment of inertia Y (m⁴)
  Iz: number   // Torsional constant (m⁴)
  Sx: number   // Section modulus X (m³)
  Sy: number   // Section modulus Y (m³)
  rx: number   // Radius of gyration X (m)
  ry: number   // Radius of gyration Y (m)
  shapeData?: number[][]  // Vertices for 3D rendering
}

// Load Types
export type LoadCaseType = 'Dead' | 'Live' | 'Wind' | 'Seismic' | 'Snow' | 'Temperature' | 'Other'

export interface LoadCase {
  id: number
  name: string
  type: LoadCaseType
  selfWeight: number  // Self-weight multiplier (typically 0 or 1)
}

export interface LoadCombination {
  id: number
  name: string
  factors: { loadCaseId: number; factor: number }[]
}

// Nodal Load
export interface NodalLoad {
  nodeId: number
  loadCaseId: number
  fx: number  // Force X
  fy: number  // Force Y
  fz: number  // Force Z
  mx: number  // Moment X
  my: number  // Moment Y
  mz: number  // Moment Z
}

// Distributed Load
export interface DistributedLoad {
  frameId: number
  loadCaseId: number
  direction: 'local' | 'global'
  axis: 'x' | 'y' | 'z'
  magnitude: number  // Force per unit length
  startPosition?: number  // Relative position (0-1)
  endPosition?: number    // Relative position (0-1)
}

// Analysis Results
export interface NodalResults {
  nodeId: number
  loadCase: string
  ux: number  // Displacement X
  uy: number  // Displacement Y
  uz: number  // Displacement Z
  rx: number  // Rotation X
  ry: number  // Rotation Y
  rz: number  // Rotation Z
}

export interface FrameResults {
  frameId: number
  loadCase: string
  station: number  // Position along frame (0-1)
  P: number   // Axial force
  V2: number  // Shear force 2
  V3: number  // Shear force 3
  T: number   // Torsion
  M2: number  // Moment 2
  M3: number  // Moment 3
}

export interface ReactionResults {
  nodeId: number
  loadCase: string
  fx: number
  fy: number
  fz: number
  mx: number
  my: number
  mz: number
}

// Project
export interface Project {
  id: string
  name: string
  units: UnitSystem
  createdAt: string
  modifiedAt: string
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  details?: Record<string, unknown>
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy'
  app: string
  version: string
}
