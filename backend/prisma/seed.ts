import { PrismaClient } from "@prisma/client";
const db = new PrismaClient();
async function main() {
  if (await db.incident.count()) return;
  const alex = await db.employee.create({ data: { name: "Alex Morgan", department: "Infrastructure" } });
  const sam = await db.employee.create({ data: { name: "Sam Lee", department: "Support" } });
  await db.incident.createMany({ data: [
    { title: "VPN access intermittent", status: "OPEN", priority: "HIGH", assigneeId: alex.id },
    { title: "Laptop provisioning delay", status: "IN_PROGRESS", priority: "MEDIUM", assigneeId: sam.id },
    { title: "Printer unavailable", status: "RESOLVED", priority: "LOW" }
  ] });
}
main().finally(() => db.$disconnect());
