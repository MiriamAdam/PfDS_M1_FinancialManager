import {categoryIcons} from "../../categoryIcons.js";
import React from "react";

export default function BudgetList({budgets}) {
    const labels =  {
        category_name: "Category",
        limit: "Limit (€)",
        remaining: "Remaining (€)",
        spent: "Spent (€)",
    }

    return (
        <div className="grid gap-4 md:grid-cols-4 p-5">
          {budgets.map((b, i) => (
            <div key={i} className="rounded-2xl shadow p-4 bg-white border border-gray-200">
              {Object.entries(b).map(([key, value]) => (
                  <div key={key} className='flex items-center mb-1'>
                      {key === "category_name" && categoryIcons[value] && (
                          <img
                            src={categoryIcons[value]}
                            alt={value}
                            className="size-10 mr-3"
                        />
                      )}
                      <p className="text-sm">
                          <span className="font-semibold">{labels[key] ?? key}: </span>
                          {typeof value === "number" ? value.toFixed(2) : String(value)}
                      </p>
                  </div>
              ))}
            </div>
          ))}
    </div>
    );
}