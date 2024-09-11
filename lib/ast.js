//  https://github.com/Mause/duckdb-ast/blob/45c5636333ce090ba3186717d521887fc0979e01/duckdb_ast/models.py
import { z } from 'zod';

export const Base = z.object({
  query_location: z.number().int().optional()
})
.strict();

export const Pair = (keySchema, valueSchema) => z.object({
  key: keySchema,
  value: valueSchema
});

// TODO: OrderedDict

export const BaseExpression = Base.extend({
  type: z.string(),
  class: z.string(),
  alias: z.string()
})

export const ParsedExpression = BaseExpression;