import {useEffect, useState} from "react";
import Toast from "./Toast.jsx";

/**
 * Form component to delete a selected budget.
 * Displays a toast notification on success.
 *
 * @param {Object} props - Component props
 * @param {function} props.onSuccess - Callback function to refresh parent data after deletion
 * @param {Array<{category_name: string}>} props.budgets - Array of budget objects available for deletion
 * @returns {JSX.Element} Delete budget form
 */
export default function DeleteBudgetForm({onSuccess, budgets}) {
    const [category_name, setCategoryName] = useState({
        category_name: '',
    });
    const [toastState, setToastState] = useState({show: false, message: '', type: 'success'});
    const handleCloseToast = () => {
        setToastState(prev => ({ ...prev, show: false }));
    };

    // Handle form submission to delete the selected budget
    const handleSubmit = async e => {
        e.preventDefault();
        const response = await fetch(`http://localhost:5000/api/budgets/${category_name}`,
            { method: 'DELETE' }
        );
        if (response.ok) {
            const data = await response.json();
            setToastState({show: true, message: data.message, type: 'success'});
            setCategoryName('');
            if (onSuccess) {
            onSuccess();
            }
        }
    }

    return (
        <>
            <form onSubmit={handleSubmit} className="flex flex-col justify-between space-y-4 p-6 bg-white rounded-lg shadow w-[50%] ">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Budget</label>
                    <select
                        value={category_name}
                        onChange={e => setCategoryName(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                        required
                    >
                        <option value="">Choose a budget</option>
                        {budgets && budgets.map(budget => (
                            <option key={budget.category_name} value={budget.category_name}>
                                {budget.category_name}
                            </option>
                        ))}
                    </select>
                </div>

                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
                >
                    Delete budget
                </button>
            </form>
            <Toast
                message={toastState.message}
                show={toastState.show}
                onClose={handleCloseToast}
                type={toastState.type}
            />
    </>
    )
}