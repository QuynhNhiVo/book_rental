/// <reference types="vite/client" />

/**
 * TypeScript type declarations for Vite environment and CSS imports
 * 
 * This file tells TypeScript how to handle:
 * 1. Vite client types and environment variables
 * 2. CSS/SCSS module imports
 * 3. Static asset imports (images, fonts, etc.)
 */

// ==================== CSS MODULE DECLARATIONS ====================
/**
 * Declare CSS modules
 * 
 * Allows TypeScript to understand when you import a .css file:
 * import './index.css'
 * 
 * Without this declaration, TypeScript throws an error:
 * "Cannot find module or its corresponding type declarations"
 */
declare module '*.css' {
  const content: string
  export default content
}

// ==================== SCSS MODULE DECLARATIONS ====================
/**
 * Declare SCSS modules (if using SCSS/SASS)
 * 
 * Enables importing SCSS files:
 * import styles from './styles.module.scss'
 */
declare module '*.scss' {
  const content: string
  export default content
}

declare module '*.sass' {
  const content: string
  export default content
}

// ==================== IMAGE ASSET DECLARATIONS ====================
/**
 * Declare image asset imports
 * 
 * Allows importing images and getting their URLs:
 * import logo from './logo.png'
 * console.log(logo) // '/src/logo.png'
 */
declare module '*.png' {
  const content: string
  export default content
}

declare module '*.jpg' {
  const content: string
  export default content
}

declare module '*.jpeg' {
  const content: string
  export default content
}

declare module '*.gif' {
  const content: string
  export default content
}

declare module '*.svg' {
  const content: string
  export default content
}

declare module '*.webp' {
  const content: string
  export default content
}

// ==================== FONT ASSET DECLARATIONS ====================
/**
 * Declare font imports
 * 
 * Enables importing font files:
 * import font from './font.woff2'
 */
declare module '*.woff' {
  const content: string
  export default content
}

declare module '*.woff2' {
  const content: string
  export default content
}

declare module '*.ttf' {
  const content: string
  export default content
}

declare module '*.otf' {
  const content: string
  export default content
}
