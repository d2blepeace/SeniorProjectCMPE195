/**
 * Modal form for creating or editing a threshold profile
 * 
 * Modal will detect:
 *  - profile.id exist -> edit mode ("save changes")
 *  - profile.id undefined -> Create mode ("create profile")
 * 
 * Prop:
 *  - profile: object with form default
 *  - onSave(formData): called on submit
 *  - onClose: called on cancelled or overlayclicj
 */

import React, {useState} from "react";
import "../styles/profileModal.css";

function ProfileModal({profile, onSave, onClose}) {
    // Local copy of form data, edit dont effect parent until click save
    const [form, setForm] = useState({...profile});
    const isEdit = !!profile.id;

    // update text field
    const updateField = (key, value) => {
        setForm((prev) => ({ ...prev, [key]: value}));
    };

    // update numeric field ('' for empty, do not allow NaN)
    const updateNumber = (key, value) => {
        setForm((prev) => ({
            ...prev,
            [key]: value=== "" ? "" : Number(value),
        }));
    };

    const handleSubmit = () => {
        if (!form.name.trim()) return;  //Name is required
        onSave(form);
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-box" onClick={(e) => e.stopPropagation()}>
                <h2 className="modal-title">
                    {isEdit ? "Edit Profile" : "Create New Profile"}
                </h2>

                {/*Profile name*/}
                <div className="form-group">
                    <label  className="form-label">Profile Name</label>
                    <input className="form-input" type="text"
                        placeholder="e.g, My Garden Setup, Lettuce Garden..."
                        value={form.name}
                        onChange={(e) => updateField("name", e.target.value)}
                    />
                </div>

                {/*optional description*/}
                <div className="form-group">
                    <label className="form-label">Description</label> 
                    <input className="form-input" type="text"
                        placeholder="Description..."
                        value={form.description || ""}
                        onChange={(e) => updateField("description", e.target.value)}
                    />
                </div>

                {/*pH ranges*/}
                <h3 className="range-header ph">pH Range</h3>
                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label">Min</label>
                        <input className="form-input" type="number"
                            step="0.1" min="0" max="14"
                            value={form.ph_min}
                            onChange={(e) => updateNumber("ph_min", e.target.value)} 
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Max</label>
                        <input className="form-input" type="number"
                            step="0.1" min="0" max="14"
                            value={form.ph_max}
                            onChange={(e) => updateNumber("ph_max", e.target.value)} 
                        />
                    </div>
                </div>

                {/*Temp Ranges*/}
                <h3 className="range-header temp">Temperature (°C)</h3>
                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label">Min</label>
                        <input className="form-input" type="number" step="0.5"
                            value={form.temp_min}
                            onChange={(e) => updateNumber("temp_min", e.target.value)} 
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Max</label>
                        <input className="form-input" type="number" step="0.5"
                            value={form.temp_max}
                            onChange={(e) => updateNumber("temp_max", e.target.value)} 
                        />
                    </div>
                </div>

                {/* Humidity Range */}
                <h3 className="range-header hum">Humidity (%)</h3>
                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label">Min</label>
                        <input className="form-input" type="number"
                            step="1" min="0" max="100"
                            value={form.humidity_min}
                            onChange={(e) => updateNumber("humidity_min", e.target.value)} 
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Max</label>
                        <input className="form-input" type="number"
                            step="1" min="0" max="100"
                            value={form.humidity_max}
                            onChange={(e) => updateNumber("humidity_max", e.target.value)} 
                        />
                    </div>
                </div>

                <div className="modal-footer">
                    <button className="btn-cancel" onClick={onClose}>
                        Cancel
                    </button>

                    <button className="btn-save" onClick={handleSubmit}>
                        {isEdit ? "Save Changes" : "Create Profile"}
                    </button>
                </div>
            </div>
        </div>

    );
}

export default ProfileModal;