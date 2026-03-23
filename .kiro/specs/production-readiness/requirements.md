# Production Readiness Specification

## Overview
Prepare the RIFFAI platform for production deployment by implementing comprehensive testing, database migrations, and GCP deployment infrastructure.

## Current Status
- ✅ Backend API (8 modules) - Complete
- ✅ Frontend (Next.js) - Complete  
- ✅ Database models (8 tables) - Complete
- ✅ Docker Compose setup - Complete
- ✅ Seed data script - Complete
- ⏳ Testing infrastructure - Partially complete (3 test files created)
- ⏳ Database migrations - Setup but not initialized
- ⏳ Production deployment - Documentation only

## User Stories

### Epic 1: Testing Infrastructure
**Priority:** HIGH  
**Status:** In Progress

#### US-1.1: Run Existing Tests
**As a** developer  
**I want to** run the existing test suite  
**So that** I can validate the current codebase works correctly

**Acceptance Criteria:**
- [ ] Test database `riffai_test` is created
- [ ] All existing tests pass without errors
- [ ] Test output shows clear pass/fail status
- [ ] No import or dependency errors

**Tasks:**
1. Create test database in Docker PostgreSQL
2. Run `pytest -v` in backend directory
3. Document any failures or issues
4. Fix any broken tests

---

#### US-1.2: Expand Test Coverage
**As a** developer  
**I want to** achieve >80% test coverage  
**So that** the codebase is reliable and maintainable

**Acceptance Criteria:**
- [ ] Overall test coverage >80%
- [ ] All API endpoints have tests
- [ ] Critical services have >90% coverage
- [ ] Coverage report generated in HTML format

**Tasks:**
1. Run `pytest --cov=app --cov-report=html`
2. Identify untested code paths
3. Write tests for:
   - Auth API endpoints
   - Map API endpoints
   - Data API endpoints
   - Alerts API endpoints
   - Water service
   - Satellite service
   - Alert service
4. Re-run coverage to verify >80%

---

### Epic 2: Database Migrations
**Priority:** HIGH  
**Status:** Not Started

#### US-2.1: Initialize Alembic Migrations
**As a** developer  
**I want to** create initial database migration  
**So that** schema changes can be tracked and deployed safely

**Acceptance Criteria:**
- [ ] Initial migration file created
- [ ] Migration includes all 8 tables
- [ ] Migration includes PostGIS extension
- [ ] Migration can be applied successfully
- [ ] Migration can be rolled back

**Tasks:**
1. Run `alembic revision --autogenerate -m "Initial schema"`
2. Review generated migration file
3. Test migration: `alembic upgrade head`
4. Test rollback: `alembic downgrade -1`
5. Re-apply: `alembic upgrade head`

---

#### US-2.2: Verify Migration in Clean Database
**As a** developer  
**I want to** test migrations on a clean database  
**So that** I know they work for new deployments

**Acceptance Criteria:**
- [ ] Can create fresh database from migrations
- [ ] All tables created correctly
- [ ] All indexes created
- [ ] PostGIS extension enabled
- [ ] Seed script works after migration

**Tasks:**
1. Drop and recreate test database
2. Run migrations on clean database
3. Verify schema matches models
4. Run seed script
5. Verify data inserted correctly

---

### Epic 3: Production Deployment
**Priority:** MEDIUM  
**Status:** Not Started

#### US-3.1: Deploy to GCP Staging
**As a** DevOps engineer  
**I want to** deploy the application to GCP staging environment  
**So that** I can test in a production-like environment

**Acceptance Criteria:**
- [ ] GCP project created
- [ ] Cloud SQL instance running
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to Vercel/Cloud Run
- [ ] Environment variables configured
- [ ] Health check endpoint accessible
- [ ] Can access API documentation

**Tasks:**
1. Create GCP project
2. Enable required APIs
3. Create Cloud SQL instance with PostGIS
4. Deploy backend to Cloud Run
5. Configure environment variables
6. Deploy frontend
7. Test end-to-end functionality

---

#### US-3.2: Setup Automated Data Pipeline
**As a** system administrator  
**I want to** automate data fetching with Cloud Scheduler  
**So that** the system stays updated without manual intervention

**Acceptance Criteria:**
- [ ] Cloud Scheduler jobs created
- [ ] Water data fetched hourly
- [ ] Satellite data fetched daily
- [ ] Predictions run daily
- [ ] Alerts checked every 15 minutes
- [ ] Jobs run successfully
- [ ] Errors logged and monitored

**Tasks:**
1. Create Cloud Scheduler job for water data
2. Create Cloud Scheduler job for satellite data
3. Create Cloud Scheduler job for predictions
4. Create Cloud Scheduler job for alert checks
5. Test each job manually
6. Monitor first 24 hours of automated runs

---

#### US-3.3: Setup Monitoring and Alerts
**As a** system administrator  
**I want to** monitor system health and receive alerts  
**So that** I can respond quickly to issues

**Acceptance Criteria:**
- [ ] Cloud Logging configured
- [ ] Error rate alerts setup
- [ ] Latency alerts setup
- [ ] Database connection alerts setup
- [ ] Alert notifications working
- [ ] Dashboard showing key metrics

**Tasks:**
1. Configure Cloud Logging
2. Create alert policy for error rate >5%
3. Create alert policy for latency >2s
4. Create alert policy for database issues
5. Setup notification channels
6. Test alert triggering

---

## Technical Requirements

### Testing
- **Framework:** pytest with pytest-asyncio
- **Coverage Tool:** pytest-cov
- **Minimum Coverage:** 80% overall, 95% for critical paths
- **Test Database:** PostgreSQL with PostGIS (riffai_test)
- **Test Types:** Unit tests, integration tests, API tests

### Database Migrations
- **Tool:** Alembic
- **Migration Strategy:** Autogenerate with manual review
- **Rollback Support:** All migrations must be reversible
- **Testing:** Test on clean database before production

### Deployment
- **Platform:** Google Cloud Platform
- **Backend:** Cloud Run (containerized FastAPI)
- **Database:** Cloud SQL PostgreSQL 15 with PostGIS
- **Cache:** Redis (Cloud Memorystore)
- **Storage:** Cloud Storage (satellite images, models, reports)
- **Scheduling:** Cloud Scheduler
- **Monitoring:** Cloud Logging + Cloud Monitoring
- **Region:** asia-southeast1 (Singapore)

### Performance Targets
- API response time: <500ms (p95)
- Database query time: <100ms (p95)
- Test execution time: <60s for full suite
- Deployment time: <10 minutes
- System uptime: >99%

### Security Requirements
- HTTPS only (enforced by Cloud Run)
- JWT authentication for protected endpoints
- Bcrypt password hashing (rounds=12)
- SQL injection protection (SQLAlchemy ORM)
- CORS configured for frontend domain only
- Secrets stored in Secret Manager (production)
- Database SSL connections (production)

## Dependencies
- All packages in `requirements.txt` must be installed
- Docker and Docker Compose for local development
- GCP account with billing enabled
- `gcloud` CLI installed and configured
- Terraform (optional, for infrastructure as code)

## Success Metrics
- [ ] All tests passing (0 failures)
- [ ] Test coverage >80%
- [ ] Migrations work on clean database
- [ ] Application deployed to staging
- [ ] Health check returns 200 OK
- [ ] API documentation accessible
- [ ] Automated jobs running successfully
- [ ] Monitoring alerts configured

## Risks and Mitigations

### Risk 1: Test Database Connection Issues
**Mitigation:** Use Docker PostgreSQL with known credentials, document setup steps clearly

### Risk 2: Migration Conflicts
**Mitigation:** Review autogenerated migrations manually, test on clean database first

### Risk 3: GCP Cost Overruns
**Mitigation:** Use free tier where possible, set budget alerts, start with minimal resources

### Risk 4: Deployment Failures
**Mitigation:** Test in staging first, have rollback plan, keep local Docker environment working

## Next Steps (Priority Order)

1. **Phase 1: Validate Testing (Week 1)**
   - Create test database
   - Run existing tests
   - Fix any failures
   - Expand test coverage to >80%

2. **Phase 2: Database Migrations (Week 1)**
   - Create initial migration
   - Test on clean database
   - Verify seed script compatibility

3. **Phase 3: Staging Deployment (Week 2)**
   - Setup GCP project
   - Deploy to Cloud Run staging
   - Configure Cloud Scheduler
   - Setup monitoring

4. **Phase 4: Production Deployment (Week 3)**
   - Deploy to production
   - Monitor for 48 hours
   - Optimize based on metrics
   - Document lessons learned

## References
- [TESTING.md](../../TESTING.md) - Testing guide
- [DEPLOYMENT.md](../../DEPLOYMENT.md) - Deployment guide
- [STATUS.md](../../STATUS.md) - Current project status
- [pytest documentation](https://docs.pytest.org/)
- [Alembic documentation](https://alembic.sqlalchemy.org/)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
