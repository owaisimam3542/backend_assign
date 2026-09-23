import { useEffect, useState } from "react";
import {
  getTriggers,
  getTemplates,
  createTrigger,
  updateTrigger,
  createTemplate,
  updateTemplate,
  testTemplate,
} from "./api";

import "./App.css";

function App() {
  const [triggers, setTriggers] = useState([]);
  const [templates, setTemplates] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // --------------------------------------------------
  // Create Trigger
  // --------------------------------------------------

  const [showTriggerForm, setShowTriggerForm] = useState(false);
  const [triggerName, setTriggerName] = useState("");
  const [triggerSlug, setTriggerSlug] = useState("");
  const [triggerDescription, setTriggerDescription] = useState("");
  const [triggerActive, setTriggerActive] = useState(true);
  const [saving, setSaving] = useState(false);

  // --------------------------------------------------
  // Edit Trigger
  // --------------------------------------------------

  const [showEditForm, setShowEditForm] = useState(false);
  const [editingTrigger, setEditingTrigger] = useState(null);
  const [editTriggerName, setEditTriggerName] = useState("");
  const [editTriggerSlug, setEditTriggerSlug] = useState("");
  const [editTriggerDescription, setEditTriggerDescription] = useState("");
  const [editTriggerActive, setEditTriggerActive] = useState(true);

  // --------------------------------------------------
  // Create / Edit Template
  // --------------------------------------------------

  const [showTemplateForm, setShowTemplateForm] = useState(false);
  const [selectedTrigger, setSelectedTrigger] = useState(null);

  const [templateChannel, setTemplateChannel] = useState("email");
  const [templateTitle, setTemplateTitle] = useState("");
  const [templateSubject, setTemplateSubject] = useState("");
  const [templateBody, setTemplateBody] = useState("");
  const [templateSaving, setTemplateSaving] = useState(false);

  const [editingTemplate, setEditingTemplate] = useState(null);
  const [isEditingTemplate, setIsEditingTemplate] = useState(false);

  // --------------------------------------------------
  // Test Notification
  // --------------------------------------------------

  const [showTestForm, setShowTestForm] = useState(false);
  const [testTrigger, setTestTrigger] = useState(null);
  const [testChannel, setTestChannel] = useState("email");
  const [testSending, setTestSending] = useState(false);

  // --------------------------------------------------
  // Load Data
  // --------------------------------------------------

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [triggerData, templateData] = await Promise.all([
        getTriggers(),
        getTemplates(),
      ]);

      setTriggers(triggerData);
      setTemplates(templateData);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to load notification data."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // --------------------------------------------------
  // Template Helpers
  // --------------------------------------------------

  const getTemplate = (triggerId, channel) => {
    return templates.find(
      (template) =>
        template.trigger === triggerId &&
        template.channel === channel
    );
  };

  // --------------------------------------------------
  // Edit Template
  // --------------------------------------------------

  const handleEditTemplate = (template) => {
    const trigger = triggers.find(
      (item) => item.id === template.trigger
    );

    setEditingTemplate(template);
    setIsEditingTemplate(true);
    setSelectedTrigger(trigger || null);

    setTemplateChannel(template.channel);
    setTemplateTitle(template.title || "");
    setTemplateSubject(template.subject || "");
    setTemplateBody(template.body || "");

    setError("");
    setShowTemplateForm(true);
  };

  // --------------------------------------------------
  // Enable / Disable Template
  // --------------------------------------------------

  const handleToggleTemplate = async (template) => {
    try {
      setError("");

      await updateTemplate(template.id, {
        trigger: template.trigger,
        channel: template.channel,
        title: template.title || "",
        subject: template.subject || "",
        body: template.body || "",
        is_enabled: !template.is_enabled,
      });

      await loadData();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to update template status."
      );
    }
  };

  // --------------------------------------------------
  // Open Test Modal
  // --------------------------------------------------

  const handleOpenTest = (trigger) => {
    setTestTrigger(trigger);
    setTestChannel("email");
    setError("");
    setShowTestForm(true);
  };

  // --------------------------------------------------
  // Send Test Notification
  // --------------------------------------------------

  const handleTestTemplate = async () => {
    if (!testTrigger) {
      return;
    }

    const template = getTemplate(
      testTrigger.id,
      testChannel
    );

    if (!template) {
      setError(
        `No ${testChannel} template exists for this trigger.`
      );
      return;
    }

    if (!template.is_enabled) {
      setError(
        `The ${testChannel} template is currently disabled. Enable it before testing.`
      );
      return;
    }

    try {
      setTestSending(true);
      setError("");

      const result = await testTemplate(template.id);

      if (result.success) {
        alert(
          `Test ${testChannel} notification sent successfully.`
        );

        setShowTestForm(false);
        setTestTrigger(null);
      } else {
        setError(
          result.message ||
            `Test ${testChannel} notification failed.`
        );
      }
    } catch (err) {
      console.error(err);

      const message =
        err.response?.data?.message ||
        err.response?.data ||
        "Failed to send test notification.";

      setError(
        typeof message === "string"
          ? message
          : JSON.stringify(message)
      );
    } finally {
      setTestSending(false);
    }
  };

  // --------------------------------------------------
  // Render Channel
  // --------------------------------------------------

  const renderChannel = (triggerId, channel) => {
    const template = getTemplate(triggerId, channel);

    if (!template) {
      return (
        <span className="disabled">
          No template
        </span>
      );
    }

    return (
      <div>
        <span
          className={
            template.is_enabled
              ? "enabled"
              : "disabled"
          }
        >
          {template.is_enabled
            ? "Enabled"
            : "Disabled"}
        </span>

        <p>{template.body}</p>

        <div className="template-actions">
          <button
            type="button"
            className="action-button"
            onClick={() =>
              handleEditTemplate(template)
            }
          >
            Edit
          </button>

          <button
            type="button"
            className="action-button"
            onClick={() =>
              handleToggleTemplate(template)
            }
          >
            {template.is_enabled
              ? "Disable"
              : "Enable"}
          </button>
        </div>
      </div>
    );
  };

  // --------------------------------------------------
  // Trigger Handlers
  // --------------------------------------------------

  const resetTriggerForm = () => {
    setTriggerName("");
    setTriggerSlug("");
    setTriggerDescription("");
    setTriggerActive(true);
  };

  const handleAddTrigger = () => {
    resetTriggerForm();
    setError("");
    setShowTriggerForm(true);
  };

  const handleCreateTrigger = async (event) => {
    event.preventDefault();

    if (!triggerName.trim()) {
      setError("Trigger name is required.");
      return;
    }

    if (!triggerSlug.trim()) {
      setError("Trigger slug is required.");
      return;
    }

    try {
      setSaving(true);
      setError("");

      await createTrigger({
        name: triggerName.trim(),
        slug: triggerSlug.trim(),
        description: triggerDescription.trim(),
        is_active: triggerActive,
      });

      setShowTriggerForm(false);
      resetTriggerForm();

      await loadData();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to create trigger."
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEditTrigger = (trigger) => {
    setEditingTrigger(trigger);

    setEditTriggerName(trigger.name);
    setEditTriggerSlug(trigger.slug);
    setEditTriggerDescription(
      trigger.description || ""
    );
    setEditTriggerActive(trigger.is_active);

    setError("");
    setShowEditForm(true);
  };

  const handleUpdateTrigger = async (event) => {
    event.preventDefault();

    if (!editingTrigger) {
      return;
    }

    if (!editTriggerName.trim()) {
      setError("Trigger name is required.");
      return;
    }

    if (!editTriggerSlug.trim()) {
      setError("Trigger slug is required.");
      return;
    }

    try {
      setSaving(true);
      setError("");

      await updateTrigger(editingTrigger.id, {
        name: editTriggerName.trim(),
        slug: editTriggerSlug.trim(),
        description: editTriggerDescription.trim(),
        is_active: editTriggerActive,
      });

      setShowEditForm(false);
      setEditingTrigger(null);

      await loadData();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to update trigger."
      );
    } finally {
      setSaving(false);
    }
  };

  // --------------------------------------------------
  // Template Handlers
  // --------------------------------------------------

  const handleAddTemplate = (trigger) => {
    setEditingTemplate(null);
    setIsEditingTemplate(false);

    setSelectedTrigger(trigger);

    setTemplateChannel("email");
    setTemplateTitle("");
    setTemplateSubject("");
    setTemplateBody("");

    setError("");
    setShowTemplateForm(true);
  };

  const handleCreateTemplate = async (event) => {
    event.preventDefault();

    if (!selectedTrigger) {
      return;
    }

    if (!templateBody.trim()) {
      setError("Template message is required.");
      return;
    }

    try {
      setTemplateSaving(true);
      setError("");

      await createTemplate({
        trigger: selectedTrigger.id,
        channel: templateChannel,
        title: templateTitle.trim(),
        subject: templateSubject.trim(),
        body: templateBody.trim(),
        is_enabled: true,
      });

      setShowTemplateForm(false);
      setSelectedTrigger(null);

      setTemplateChannel("email");
      setTemplateTitle("");
      setTemplateSubject("");
      setTemplateBody("");

      await loadData();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to create template."
      );
    } finally {
      setTemplateSaving(false);
    }
  };

  const handleUpdateTemplate = async (event) => {
    event.preventDefault();

    if (!editingTemplate) {
      return;
    }

    if (!templateBody.trim()) {
      setError("Template message is required.");
      return;
    }

    try {
      setTemplateSaving(true);
      setError("");

      await updateTemplate(editingTemplate.id, {
        trigger: editingTemplate.trigger,
        channel: templateChannel,
        title: templateTitle.trim(),
        subject: templateSubject.trim(),
        body: templateBody.trim(),
        is_enabled: editingTemplate.is_enabled,
      });

      setShowTemplateForm(false);
      setEditingTemplate(null);
      setIsEditingTemplate(false);
      setSelectedTrigger(null);

      setTemplateChannel("email");
      setTemplateTitle("");
      setTemplateSubject("");
      setTemplateBody("");

      await loadData();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to update template."
      );
    } finally {
      setTemplateSaving(false);
    }
  };

  // --------------------------------------------------
  // Modal Close Helpers
  // --------------------------------------------------

  const closeTriggerModal = () => {
    setShowTriggerForm(false);
    resetTriggerForm();
    setError("");
  };

  const closeEditTriggerModal = () => {
    setShowEditForm(false);
    setEditingTrigger(null);
    setError("");
  };

  const closeTemplateModal = () => {
    setShowTemplateForm(false);
    setSelectedTrigger(null);
    setEditingTemplate(null);
    setIsEditingTemplate(false);

    setTemplateChannel("email");
    setTemplateTitle("");
    setTemplateSubject("");
    setTemplateBody("");

    setError("");
  };

  const closeTestModal = () => {
    setShowTestForm(false);
    setTestTrigger(null);
    setTestChannel("email");
    setError("");
  };

  // --------------------------------------------------
  // Render
  // --------------------------------------------------

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Notification Management</h1>

          <p>
            Manage notification triggers and templates
          </p>
        </div>

        <button
          className="add-trigger-button"
          onClick={handleAddTrigger}
        >
          + Add Trigger
        </button>
      </header>

      <main className="content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading notifications...
          </div>
        ) : (
          <div className="table-container">
            <table className="notification-table">
              <thead>
                <tr>
                  <th>Trigger</th>
                  <th>WhatsApp</th>
                  <th>Email</th>
                  <th>Web Push</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {triggers.length === 0 ? (
                  <tr>
                    <td
                      colSpan="5"
                      className="empty-state"
                    >
                      No notification triggers found.
                    </td>
                  </tr>
                ) : (
                  triggers.map((trigger) => (
                    <tr key={trigger.id}>
                      <td>
                        <div className="trigger-name">
                          {trigger.name}
                        </div>

                        <div className="trigger-slug">
                          {trigger.slug}
                        </div>

                        {trigger.description && (
                          <div className="trigger-description">
                            {trigger.description}
                          </div>
                        )}

                        <span
                          className={
                            trigger.is_active
                              ? "enabled"
                              : "disabled"
                          }
                        >
                          {trigger.is_active
                            ? "Active"
                            : "Inactive"}
                        </span>
                      </td>

                      <td>
                        {renderChannel(
                          trigger.id,
                          "whatsapp"
                        )}
                      </td>

                      <td>
                        {renderChannel(
                          trigger.id,
                          "email"
                        )}
                      </td>

                      <td>
                        {renderChannel(
                          trigger.id,
                          "web_push"
                        )}
                      </td>

                      <td>
                        <div className="actions">
                          <button
                            type="button"
                            className="action-button"
                            onClick={() =>
                              handleEditTrigger(
                                trigger
                              )
                            }
                          >
                            Edit
                          </button>

                          <button
                            type="button"
                            className="action-button"
                            onClick={() =>
                              handleAddTemplate(
                                trigger
                              )
                            }
                          >
                            Template
                          </button>

                          <button
                            type="button"
                            className="action-button"
                            onClick={() =>
                              handleOpenTest(trigger)
                            }
                          >
                            Test
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {/* --------------------------------------------------
          ADD TRIGGER MODAL
      -------------------------------------------------- */}

      {showTriggerForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add Notification Trigger</h2>

            <form onSubmit={handleCreateTrigger}>
              <label>Trigger Name</label>

              <input
                type="text"
                value={triggerName}
                onChange={(event) =>
                  setTriggerName(event.target.value)
                }
                placeholder="e.g. User Login"
              />

              <label>Slug</label>

              <input
                type="text"
                value={triggerSlug}
                onChange={(event) =>
                  setTriggerSlug(event.target.value)
                }
                placeholder="e.g. user-login"
              />

              <label>Description</label>

              <textarea
                rows="4"
                value={triggerDescription}
                onChange={(event) =>
                  setTriggerDescription(
                    event.target.value
                  )
                }
                placeholder="Describe when this trigger fires"
              />

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={triggerActive}
                  onChange={(event) =>
                    setTriggerActive(
                      event.target.checked
                    )
                  }
                />

                Active
              </label>

              <div className="modal-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeTriggerModal}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-button"
                  disabled={saving}
                >
                  {saving
                    ? "Saving..."
                    : "Create Trigger"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --------------------------------------------------
          EDIT TRIGGER MODAL
      -------------------------------------------------- */}

      {showEditForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Edit Notification Trigger</h2>

            <form onSubmit={handleUpdateTrigger}>
              <label>Trigger Name</label>

              <input
                type="text"
                value={editTriggerName}
                onChange={(event) =>
                  setEditTriggerName(
                    event.target.value
                  )
                }
                placeholder="e.g. User Login"
              />

              <label>Slug</label>

              <input
                type="text"
                value={editTriggerSlug}
                onChange={(event) =>
                  setEditTriggerSlug(
                    event.target.value
                  )
                }
                placeholder="e.g. user-login"
              />

              <label>Description</label>

              <textarea
                rows="4"
                value={editTriggerDescription}
                onChange={(event) =>
                  setEditTriggerDescription(
                    event.target.value
                  )
                }
                placeholder="Describe when this trigger fires"
              />

              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={editTriggerActive}
                  onChange={(event) =>
                    setEditTriggerActive(
                      event.target.checked
                    )
                  }
                />

                Active
              </label>

              <div className="modal-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeEditTriggerModal}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-button"
                  disabled={saving}
                >
                  {saving
                    ? "Saving..."
                    : "Save Changes"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --------------------------------------------------
          CREATE / EDIT TEMPLATE MODAL
      -------------------------------------------------- */}

      {showTemplateForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>
              {isEditingTemplate
                ? "Edit Notification Template"
                : "Add Notification Template"}
            </h2>

            <form
              onSubmit={
                isEditingTemplate
                  ? handleUpdateTemplate
                  : handleCreateTemplate
              }
            >
              <label>Trigger</label>

              <input
                type="text"
                value={
                  selectedTrigger
                    ? selectedTrigger.name
                    : ""
                }
                disabled
              />

              <label>Channel</label>

              <select
                value={templateChannel}
                onChange={(event) =>
                  setTemplateChannel(
                    event.target.value
                  )
                }
                disabled={isEditingTemplate}
              >
                <option value="email">
                  Email
                </option>

                <option value="whatsapp">
                  WhatsApp
                </option>

                <option value="web_push">
                  Web Push
                </option>
              </select>

              <label>Title</label>

              <input
                type="text"
                value={templateTitle}
                onChange={(event) =>
                  setTemplateTitle(
                    event.target.value
                  )
                }
                placeholder="Notification title"
              />

              <label>Subject</label>

              <input
                type="text"
                value={templateSubject}
                onChange={(event) =>
                  setTemplateSubject(
                    event.target.value
                  )
                }
                placeholder="Email subject"
              />

              <label>Message</label>

              <textarea
                rows="6"
                value={templateBody}
                onChange={(event) =>
                  setTemplateBody(
                    event.target.value
                  )
                }
                placeholder="Hello {{user_name}}, ..."
              />

              <div className="modal-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeTemplateModal}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-button"
                  disabled={templateSaving}
                >
                  {templateSaving
                    ? "Saving..."
                    : isEditingTemplate
                    ? "Save Changes"
                    : "Create Template"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --------------------------------------------------
          TEST NOTIFICATION MODAL
      -------------------------------------------------- */}

      {showTestForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Test Notification</h2>

            <p>
              {testTrigger
                ? `Choose a channel to test for "${testTrigger.name}".`
                : "Choose a notification channel."}
            </p>

            <label>Channel</label>

            <select
              value={testChannel}
              onChange={(event) =>
                setTestChannel(event.target.value)
              }
            >
              <option value="email">
                Email
              </option>

              <option value="whatsapp">
                WhatsApp
              </option>

              <option value="web_push">
                Web Push
              </option>
            </select>

            {testTrigger && (
              <div
                style={{
                  marginTop: "15px",
                  padding: "12px",
                  background: "#f3f4f6",
                  borderRadius: "6px",
                }}
              >
                <strong>Selected template:</strong>

                <p style={{ marginBottom: 0 }}>
                  {getTemplate(
                    testTrigger.id,
                    testChannel
                  )
                    ? "Template available"
                    : "No template configured"}
                </p>
              </div>
            )}

            <div className="modal-actions">
              <button
                type="button"
                className="cancel-button"
                onClick={closeTestModal}
                disabled={testSending}
              >
                Cancel
              </button>

              <button
                type="button"
                className="save-button"
                onClick={handleTestTemplate}
                disabled={testSending}
              >
                {testSending
                  ? "Sending..."
                  : "Send Test"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;