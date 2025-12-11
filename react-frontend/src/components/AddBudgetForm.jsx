import {useEffect, useState} from "react";
import Toast from "./Toast.jsx";

/**
 * Form component to add a new budget for a category.
 * Only expense categories (excluding "Sales" and "Income") are available.
 * Displays success or error toast messages on submission.
 *
 * @param {Object} props - Component props
 * @param {function} props.onSuccess - Callback invoked after successfully adding a budget
 * @returns {JSX.Element} AddBudgetForm component
 */
export default function AddBudgetForm({onSuccess}) {
    const [categories, setCategories] = useState([]);
    const [formData, setFormData] = useState({
        category_name: '',
        limit: ''
    });
    const [toastMessage, setToastMessage] = useState("");
    const [toastType, setToastType] = useState("error");
    const [showToast, setShowToast] = useState(false);

    // Fetch expense categories on component mount
    useEffect(() => {
        fetch('http://localhost:5000/api/categories')
            .then(res => res.json())
            .then(data => {
                const only_expenses = data.filter(
                    cat => cat.category_name !== 'Sales' && cat.category_name !== 'Income');
                setCategories(only_expenses);
            })
            .catch(err => console.log(err));
    }, []);

     /**
     * Handles category selection change.
     * Resets the limit field when category changes.
     *
     * @param {Event} e - Change event from category select
     */
    const handleCategoryChange = (e) => {
        const category_name = e.target.value;
        setFormData({...formData, category_name, limit: ''});
    }

    /**
     * Handles form submission.
     * Sends POST request to add a new budget and displays toast messages.
     *
     * @param {Event} e - Form submission event
     */
    const handleSubmit = async e => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/api/budgets', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });

        const body = await response.json();

        if (response.ok) {
            setToastMessage(body.message);
            setToastType("success");
            setShowToast(true);
            setFormData({category_name: '', limit: ''});
            if (onSuccess) {
            onSuccess();
            }
        }
        else if (response.status === 409) {
            setToastMessage(body.error);
            setToastType("error");
            setShowToast(true);
        }
    }

    return (
        <>
        <form onSubmit={handleSubmit} className="space-y-4 p-6 bg-white rounded-lg shadow w-[50%] ">
            <div>
                <label className="block text-sm font-medium text-gray-700">Category</label>
                <select
                    value={formData.category_name}
                    onChange={handleCategoryChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    required
                >
                    <option value="">Choose a category</option>
                    {categories.map(cat => (
                        <option key={cat.category_name} value={cat.category_name}>
                          {cat.category_name}
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Limit (€)</label>
                <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={formData.limit}
                    onChange={(e) => {
                        let value = parseFloat(e.target.value);
                        setFormData({...formData, limit: String(value)})}}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-center"
                    required
                />
            </div>

            <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
                Add budget
            </button>
        </form>
        <Toast
            message={toastMessage}
            show={showToast}
            onClose={() => setShowToast(false)}
            type={toastType}
          />
        </>
    )
}