import { create } from 'zustand'

/**
 * Project state management using Zustand.
 * Manages the current project and its structural model.
 */

export interface Node {
  id: number
  x: number
  y: number
  z: number
  restraint: {
    ux: boolean
    uy: boolean
    uz: boolean
    rx: boolean
    ry: boolean
    rz: boolean
  }
}

export interface Frame {
  id: number
  nodeI: number
  nodeJ: number
  materialId: string
  sectionId: string
  rotation: number
}

export interface Project {
  id: string | null
  name: string
  units: {
    length: string
    force: string
    angle: string
  }
  nodes: Node[]
  frames: Frame[]
  isDirty: boolean
}

interface ProjectState extends Project {
  // Actions
  setProject: (project: Partial<Project>) => void
  addNode: (node: Node) => void
  removeNode: (id: number) => void
  updateNode: (id: number, updates: Partial<Node>) => void
  addFrame: (frame: Frame) => void
  removeFrame: (id: number) => void
  updateFrame: (id: number, updates: Partial<Frame>) => void
  resetProject: () => void
  setDirty: (dirty: boolean) => void
}

const initialState: Project = {
  id: null,
  name: 'Nuevo Proyecto',
  units: {
    length: 'm',
    force: 'kN',
    angle: 'deg',
  },
  nodes: [],
  frames: [],
  isDirty: false,
}

export const useProject = create<ProjectState>((set) => ({
  ...initialState,

  setProject: (project) =>
    set((state) => ({ ...state, ...project, isDirty: true })),

  addNode: (node) =>
    set((state) => ({
      nodes: [...state.nodes, node],
      isDirty: true,
    })),

  removeNode: (id) =>
    set((state) => ({
      nodes: state.nodes.filter((n) => n.id !== id),
      isDirty: true,
    })),

  updateNode: (id, updates) =>
    set((state) => ({
      nodes: state.nodes.map((n) => (n.id === id ? { ...n, ...updates } : n)),
      isDirty: true,
    })),

  addFrame: (frame) =>
    set((state) => ({
      frames: [...state.frames, frame],
      isDirty: true,
    })),

  removeFrame: (id) =>
    set((state) => ({
      frames: state.frames.filter((f) => f.id !== id),
      isDirty: true,
    })),

  updateFrame: (id, updates) =>
    set((state) => ({
      frames: state.frames.map((f) => (f.id === id ? { ...f, ...updates } : f)),
      isDirty: true,
    })),

  resetProject: () => set(initialState),

  setDirty: (dirty) => set({ isDirty: dirty }),
}))

export default useProject
