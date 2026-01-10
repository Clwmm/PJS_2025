const BASE_URL = import.meta.env.VITE_BACKEND_URL;

if (!BASE_URL) {
    throw new Error("VITE_BACKEND_URL is not defined");
}

export async function apiPost(endpoint, body) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error");
    }

    return res.json();
}
