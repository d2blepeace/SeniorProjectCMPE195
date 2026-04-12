/**
 * ConfirmDialog Component
 * Prop:
 *  - title
 *  - message: string or JSX
 *  - confirmLabel
 *  - onConfirm()
 *  - onCancel(
 */
import React from "react";
import "../styles/confirmDialog.css";

function ConfirmDialog({ title, message, confirmLabel = "Delete", onConfirm, onCancel }) {
    return (
        <div className="confirm-overlay" onClick={onCancel}>
            <div className="confirm-box" onClick={(e) => e.stopPropagation()}>
                <h3 className="confirm-title">{title}</h3>
                <p className="confirm-message">{message}</p>
                <div className="confirm-actions">
                    <button className="btn-cancel" onClick={onCancel}>Cancel</button>
                    <button className="btn-confirm-delete" onClick={onConfirm}>
                        {confirmLabel}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ConfirmDialog;