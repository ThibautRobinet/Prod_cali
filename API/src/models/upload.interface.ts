// src/items/items.interface.ts

export interface BaseFile {
  image: string;
}

export interface File extends BaseFile {
  id: number;
}