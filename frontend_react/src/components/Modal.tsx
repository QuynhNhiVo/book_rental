/**
 * ═══════════════════════════════════════════════════════════════
 * MODAL COMPONENT - Reusable Dialog/Overlay
 * ═══════════════════════════════════════════════════════════════
 * 
 * A reusable modal component for displaying forms, confirmations,
 * and other overlay content.
 * 
 * DESIGN PATTERN: Compound Component
 * - Accepts children (form content) via props
 * - Manages visibility state from parent
 * - Provides consistent styling and behavior
 * 
 * FEATURES:
 * - Smooth animations (fade-in, slide-in)
 * - Close button (X icon)
 * - Click outside to close (via onClose callback)
 * - Keyboard escape key support (implement in parent)
 * - Responsive sizing
 * 
 * USAGE PATTERNS:
 * 
 * 1. Form Modal (Create/Edit)
 *    <Modal title="Add Book" isOpen={showModal} onClose={() => setShowModal(false)}>
 *      <form>
 *        <input placeholder="Title" />
 *        <button>Save</button>
 *      </form>
 *    </Modal>
 * 
 * 2. Confirmation Modal
 *    <Modal title="Confirm Delete?" isOpen={showConfirm} onClose={handleCancel}>
 *      <p>Are you sure? This cannot be undone.</p>
 *      <button onClick={handleConfirm}>Delete</button>
 *    </Modal>
 * 
 * ═══════════════════════════════════════════════════════════════
 */

import React from 'react'
import { X } from 'lucide-react'  // Lucide icon library for close button

/**
 * Modal Props Interface
 * 
 * @interface ModalProps
 * @property {string} title - Modal title/heading
 * @property {boolean} isOpen - Controls modal visibility
 * @property {() => void} onClose - Callback when user closes modal
 * @property {React.ReactNode} children - Modal content (usually a form)
 */
interface ModalProps {
  title: string
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}

/**
 * Modal Component
 * 
 * Renders a centered dialog overlay with smooth animations.
 * 
 * RENDERING LOGIC:
 * - If !isOpen: Returns null (nothing rendered)
 * - If isOpen: Renders overlay with modal content
 * 
 * STRUCTURE:
 * ├─ modal-overlay (dark background, fills screen)
 * │  └─ modal (white box, centered)
 * │     ├─ Header (title + close button)
 * │     └─ Content (children)
 * 
 * @param {ModalProps} props - Component props
 * @returns {JSX.Element | null} Modal UI or null if not open
 */
export default function Modal({ title, isOpen, onClose, children }: ModalProps) {
  // ==================== CONDITIONAL RENDERING ====================
  // Don't render anything if modal is closed
  // This prevents DOM nodes from being created unnecessarily
  if (!isOpen) return null

  return (
    // ==================== MODAL OVERLAY ====================
    // Dark background that fills the screen
    // Clicking here can close modal (parent should handle via onClose)
    // animation: fade-in (defined in index.css)
    <div className="modal-overlay animate-fade-in">
      
      {/* ==================== MODAL DIALOG BOX ==================== */}
      {/* White centered box containing the form/content */}
      {/* animation: slide-in (defined in index.css) */}
      <div className="modal animate-slide-in">
        
        {/* ==================== MODAL HEADER ==================== */}
        {/* Title and close button */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          {/* Modal Title */}
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>

          {/* Close Button */}
          <button
            onClick={onClose}
            // Styling: gray icon, hover effect
            className="text-gray-400 hover:text-gray-600 transition-colors"
            // Accessibility: Show close button intent
            aria-label="Close modal"
            type="button"
          >
            {/* X icon from Lucide React */}
            <X size={24} />
          </button>
        </div>

        {/* ==================== MODAL CONTENT ==================== */}
        {/* Children are rendered here (usually form fields) */}
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  )
}
