export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface ITable {
  id: number;
  owner_id: number;
  digits: string;
}

export interface IInstruction {
  id: number;
  owner_id: number;
  description: string;
}

export interface IInfo {
  errors: string;
  choosed_number: string;
  time: number;
  table_id: number;
}

export interface ITestResponse {
  errors: string;
  choosed_number: string;
  time: number;
  table_id: number;
  id: number;
  owner_id: number;
}

export interface IAttemptResponse {
  attempt_id: number;
}
