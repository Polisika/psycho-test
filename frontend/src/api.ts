import axios, { AxiosResponse } from "axios";
import { apiUrl } from "@/env";
import {
  IInfo,
  IInstruction,
  ITestResponse,
  IUserProfile,
  IUserProfileCreate,
  IUserProfileUpdate,
} from "./interfaces";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token),
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getInstructions() {
    const response: AxiosResponse<IInstruction> = await axios.get(
      `${apiUrl}/api/v1/instruction/`,
    );
    return response.data.description;
  },
  async getTable(token: string) {
    return await axios.post(`${apiUrl}/api/v1/tables/generate`, {}, authHeaders(token));
  },
  async createTests(token: string, tests: Array<IInfo>) {
    const ids: Array<number> = [];
    for (const info of tests) {
      const result: AxiosResponse<ITestResponse> = await axios.post(
        `${apiUrl}/api/v1/test`,
        info,
        authHeaders(token),
      );
      console.log(`TEST CREATED ${result.data.id}`);
      ids.push(result.data.id);
    }
    return await axios.post(
      `${apiUrl}/api/v1/attempt`,
      { tests: ids },
      authHeaders(token),
    );
  },
  async getAnalytic(token: string, attempt_id: number) {
    const r = await axios.get(`${apiUrl}/api/v1/attempt`, authHeaders(token));
    const result: Array<ITestResponse> = [];
    for (const item of r.data.filter((x) => x.id == attempt_id)) {
      const resp: AxiosResponse<ITestResponse> = await axios.get(
        `${apiUrl}/api/v1/test/${item.test_id}`,
        authHeaders(token),
      );
      result.push(resp.data);
    }
    return result;
  },
  async setInstructions(token: string, instructions: string) {
    return await axios.put(
      `${apiUrl}/api/v1/instruction/1`,
      { description: instructions },
      authHeaders(token),
    );
  },
};
