import {requestAPI} from "./handler";

export async function fetchTokenLocation(): Promise<string> {
    const data = await requestAPI<any>('vdkAccessTokenLocation', {
        method: 'GET'
    });
    if (data) {
        return data || '';
    } else {
        console.error("Couldn't fetch token location from the server");
        return '';
    }
}


function safeJSONParse<T = any>(value: string | null): T | null {
    try {
        return JSON.parse(value || 'null');
    } catch {
        return null;
    }
}

export async function getTokenFromLocation(location: string): Promise<string | null> {
    const parts = location.split(':');
    const storageType = parts[0];
    const path = parts[1].split('.');

    if (storageType === "localStorage") {
        let item = safeJSONParse(window.top.localStorage.getItem(path[0]));
        return path.reduce((current, key) => {
            return current && key in current ? current[key] : null;
        }, item);
    }
    return null;
}

export async function sendTokenToServer(token: string): Promise<void> {
    try {
        await requestAPI<any>('vdkAccessToken', {
            body: JSON.stringify({ token }),
            method: 'POST'
        });
    } catch (error) {
        console.error("Couldn't send token to server", error);
    }
}



const CHECK_INTERVAL_MS = 60000;

/**
 * Checks for the presence of a token and sends it to the server if found.
 *
 * This function fetches the token location, retrieves the token from the specified location,
 * and sends the token to the server.
 *
 * @returns {Promise<string>} - Returns the token location. If the token is not found then we should not schedule regular update.
 */
async function checkToken() {
    const tokenLocation = await fetchTokenLocation();
    console.debug("Checking VDK token location")
    if (tokenLocation) {
        const token = await getTokenFromLocation(tokenLocation);

        if (token) {
            console.debug("VDK token found. Sending it to the server")
            await sendTokenToServer(token);
            console.debug("Sent VDK token to the server")
        }
    }
    return tokenLocation
}

/**
 * Setups regularly to update the access token from the parent
 */
export async function setupTokenCheckInterval() {
    const initialTokenLocation = await checkToken();  // Run immediately

    if (initialTokenLocation) {
        console.log("Initial token location is " + initialTokenLocation)
        console.log("Schedule regular update every " + CHECK_INTERVAL_MS)
        setInterval(checkToken, CHECK_INTERVAL_MS);
    } else {
        console.log("No token location. Disable regular token update")
    }
}
