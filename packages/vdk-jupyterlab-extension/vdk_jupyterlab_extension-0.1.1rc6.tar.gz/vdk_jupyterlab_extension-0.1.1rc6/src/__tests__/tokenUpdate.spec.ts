import {fetchTokenLocation, getTokenFromLocation, sendTokenToServer, setupTokenCheckInterval} from "../tokenUpdate";
import { requestAPI } from '../handler';

// Mocking requestAPI
jest.mock("../handler", () => ({
    requestAPI: jest.fn()
}));

// Mocking localStorage
const mockLocalStorage = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    clear: jest.fn()
};

Object.defineProperty(window, 'localStorage', {
    value: mockLocalStorage,
});

describe("VDK Access Token Handling", () => {

    beforeEach(() => {
        jest.clearAllMocks();
        jest.restoreAllMocks();
        jest.useFakeTimers();
    });
    afterEach(() => {
        jest.clearAllMocks();
        jest.restoreAllMocks();
    });

    it("fetches token location", async () => {
        (requestAPI as jest.Mock).mockResolvedValue('localStorage:token.path');

        const location = await fetchTokenLocation();

        expect(location).toBe('localStorage:token.path');
        expect(requestAPI).toHaveBeenCalledWith('vdkAccessTokenLocation', { method: 'GET' });
    });

    it("handles errors when fetching token location", async () => {
        (requestAPI as jest.Mock).mockRejectedValue(new Error("Failed fetch token location request"));

        await expect(fetchTokenLocation()).rejects.toThrow("Failed fetch token location request")

        expect(requestAPI).toHaveBeenCalledWith('vdkAccessTokenLocation', { method: 'GET' });
    });

    it("gets token from localStorage", async () => {
        mockLocalStorage.getItem.mockReturnValue(JSON.stringify({token: { path: "myToken" }}));

        const token = await getTokenFromLocation('localStorage:token.path');

        expect(token).toBe("myToken");
    });

    it("handles non-existent token paths in localStorage", async () => {
        mockLocalStorage.getItem.mockReturnValue(JSON.stringify({}));

        const token = await getTokenFromLocation('localStorage:token.path');

        expect(token).toBeNull();
    });

    it("sends token to server", async () => {
        (requestAPI as jest.Mock).mockResolvedValue(true);

        await sendTokenToServer('myToken');

        expect(requestAPI).toHaveBeenCalledWith('vdkAccessToken', {
            body: JSON.stringify({ token: 'myToken' }),
            method: 'POST'
        });
    });

    it("handles errors when sending token to server", async () => {
        (requestAPI as jest.Mock).mockRejectedValue(new Error("Failed sending token request"));

        const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        await sendTokenToServer('myToken');
        consoleErrorSpy.mockRestore()

        expect(requestAPI).toHaveBeenCalledWith('vdkAccessToken', {
            body: JSON.stringify({ token: 'myToken' }),
            method: 'POST'
        });
    });

    it("sets up token check interval and checks token flow", async () => {
        (requestAPI as jest.Mock).mockResolvedValueOnce('localStorage:path');
        mockLocalStorage.getItem.mockReturnValueOnce(JSON.stringify({ path: "myToken" }));
        (requestAPI as jest.Mock).mockResolvedValueOnce(true);

        await setupTokenCheckInterval();

        jest.advanceTimersByTime(60000);

        expect(requestAPI).toHaveBeenNthCalledWith(1, 'vdkAccessTokenLocation', { method: 'GET' });
        expect(requestAPI).toHaveBeenNthCalledWith(2, 'vdkAccessToken', {
            body: JSON.stringify({ token: 'myToken' }),
            method: 'POST'
        });
    });

});
