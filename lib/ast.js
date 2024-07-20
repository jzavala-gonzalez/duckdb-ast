import { z } from 'zod';

export const Base = z.object({
  query_location: z.number().int().optional()
})
.strict();