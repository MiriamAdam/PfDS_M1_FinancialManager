import { useEffect } from "react";
import classNames from "classnames";

/**
 * Toast component for temporary notifications.
 * Automatically disappears after 3 seconds when `show` is true.
 *
 * @param {Object} props - Component props
 * @param {string} props.message - Text message to display in the toast
 * @param {boolean} props.show - Whether the toast is visible
 * @param {function} props.onClose - Callback function called when the toast closes
 * @param {"success"|"error"} props.type - Type of toast, determines background color
 * @returns {JSX.Element|null} Toast notification or null if not visible
 */
export default function Toast({ message, show, onClose, type }) {
  // Automatically hide the toast after 3 seconds
    useEffect(() => {
    if (!show) return;

    const timer = setTimeout(() => {
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div className={classNames('fixed bottom-6 right-6 text-white px-4 py-3 rounded-xl shadow-lg animate-fadeIn', {"bg-green-600": type === "success", "bg-red-600": type ==="error"})}>
      {message}
    </div>
  );
}