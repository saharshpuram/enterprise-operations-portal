import express from "express";
import cors from "cors";
import { PrismaClient } from "@prisma/client";
const app = express();
const db = new PrismaClient();
app.use(cors({ origin: process.env.CORS_ORIGIN ?? "http://localhost:5173" }));
app.use(express.json());
app.get("/health", (_req, res) => res.json({ status: "ok" }));
app.get("/api/incidents", async (_req, res, next) => {
  try {
    const incidents = await db.incident.findMany({ orderBy: { id: "asc" }, include: { assignee: true } });
    res.json(incidents.map(({ assignee, ...incident }) => ({ ...incident, assigneeName: assignee?.name ?? null })));
  } catch (error) { next(error); }
});
app.patch("/api/incidents/:id/status", async (req, res, next) => {
  try {
    const id = Number(req.params.id);
    const status = req.body?.status;
    if (!Number.isInteger(id) || id < 1 || !["OPEN", "IN_PROGRESS", "RESOLVED"].includes(status)) {
      res.status(400).json({ error: "Invalid incident id or status" }); return;
    }
    const incident = await db.incident.update({ where: { id }, data: { status } });
    res.json(incident);
  } catch (error) {
    if (typeof error === "object" && error !== null && "code" in error && error.code === "P2025") {
      res.status(404).json({ error: "Incident not found" }); return;
    }
    next(error);
  }
});
app.use((_err: unknown, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  res.status(500).json({ error: "Internal server error" });
});
app.listen(Number(process.env.PORT ?? 3000), "0.0.0.0", () => console.log("API listening"));
