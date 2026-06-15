export interface Task {
  id: number;
  title: string;
  description: string | null;
  position: number;
  column_id: number;
  created_at: string;
}

export interface Column {
  id: number;
  title: string;
  position: number;
  tasks: Task[];
}