import { useEffect } from "react";
import classNames from "classnames";

export default function Toast({ message, show, onClose, type }) {
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