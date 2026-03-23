# Production Readiness - Implementation Plan

## Current Session: Phase 1 - Validate Testing

### Immediate Next Steps

#### Step 1: Create Test Database ✓ Ready
```bash
cd riffai-platform/infrastructure/docker
docker compose up -d
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"
```

**Expected Result:** Test database created successfully

---

#### Step 2: Run Existing Tests
```bash
cd riffai-platform/backend
pytest -v
```

**Expected Result:** 
- 3 test files execute
- ~5-7 tests run
- May have some failures (expected, will fix)

**Possible Issues:**
- Import errors → Check PYTHONPATH
- Database connection errors → Verify test database exists
- Missing dependencies → Run `pip install -r requirements.txt`

---

#### Step 3: Analyze Test Results
Review test output and identify:
- Which tests pass ✅
- Which tests fail ❌
- What errors occur
- What's the current coverage %

---

#### Step 4: Fix Failing Tests
Based on failures, fix:
- Import issues
- Database schema mismatches
- Missing fixtures
- Incorrect assertions

---

#### Step 5: Run Coverage Report
```bash
pytest --cov=app --cov-report=html --cov-report=term
```

**Expected Result:**
- Coverage report generated
- Current coverage % displayed
- HTML report in `htmlcov/` directory

---

### Phase 1 Success Criteria
- [ ] Test database created
- [ ] All existing tests pass
- [ ] Coverage report generated
- [ ] Current coverage % known
- [ ] Ready to expand test coverage

---

## Phase 2: Expand Test Coverage (After Phase 1)

### Files Needing Tests
1. `app/api/endpoints/auth.py` - Authentication endpoints
2. `app/api/endpoints/map.py` - Map/GIS endpoints
3. `app/api/endpoints/data.py` - Data analytics endpoints
4. `app/api/endpoints/alerts.py` - Alert endpoints
5. `app/api/endpoints/prediction.py` - Prediction endpoints (when implemented)
6. `app/services/water_service.py` - Water data service
7. `app/services/satellite_service.py` - Satellite service
8. `app/services/alert_service.py` - Alert service

### Test File Structure
```
tests/
├── test_api/
│   ├── test_auth.py          # NEW
│   ├── test_map.py           # NEW
│   ├── test_data.py          # NEW
│   ├── test_alerts.py        # NEW
│   ├── test_dashboard.py     # EXISTS
│   └── test_prediction.py    # EXISTS
├── test_services/
│   ├── test_ai_service.py    # EXISTS
│   ├── test_water_service.py # NEW
│   ├── test_satellite_service.py # NEW
│   └── test_alert_service.py # NEW
└── test_models/
    └── test_database.py      # NEW
```

---

## Phase 3: Database Migrations (After Phase 2)

### Step 1: Create Initial Migration
```bash
cd riffai-platform/backend
alembic revision --autogenerate -m "Initial schema"
```

### Step 2: Review Migration
- Check generated file in `alembic/versions/`
- Verify all tables included
- Verify PostGIS extension
- Add manual fixes if needed

### Step 3: Test Migration
```bash
# Apply
alembic upgrade head

# Rollback
alembic downgrade -1

# Re-apply
alembic upgrade head
```

### Step 4: Test on Clean Database
```bash
# Drop and recreate
docker exec -it docker-db-1 psql -U riffai -c "DROP DATABASE IF EXISTS riffai_test;"
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"

# Run migrations
alembic upgrade head

# Run seed
python -m app.seed
```

---

## Phase 4: GCP Staging Deployment (After Phase 3)

### Prerequisites
- GCP account with billing enabled
- `gcloud` CLI installed
- Project ID chosen

### Steps
1. Create GCP project
2. Enable APIs
3. Create Cloud SQL instance
4. Deploy backend to Cloud Run
5. Deploy frontend to Vercel
6. Configure environment variables
7. Test end-to-end

---

## Decision Points

### After Step 2 (Run Tests)
**If all tests pass:**
→ Proceed to Step 5 (Coverage Report)

**If tests fail:**
→ Proceed to Step 4 (Fix Failing Tests)

### After Phase 1
**If coverage >80%:**
→ Skip Phase 2, proceed to Phase 3 (Migrations)

**If coverage <80%:**
→ Proceed to Phase 2 (Expand Coverage)

### After Phase 3
**If user wants to deploy:**
→ Proceed to Phase 4 (GCP Deployment)

**If user wants to continue development:**
→ Return to feature development

---

## Commands Quick Reference

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api/test_dashboard.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run and show print statements
pytest -v -s
```

### Database
```bash
# Create test database
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"

# Drop test database
docker exec -it docker-db-1 psql -U riffai -c "DROP DATABASE IF EXISTS riffai_test;"

# List databases
docker exec -it docker-db-1 psql -U riffai -l
```

### Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show migration history
alembic history

# Show current version
alembic current
```

### Docker
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f backend

# Rebuild and start
docker compose up --build
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
```bash
cd backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest
```

### "Database does not exist"
```bash
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"
```

### "Connection refused" to database
```bash
# Check if PostgreSQL is running
docker compose ps

# Restart if needed
docker compose restart db
```

### Tests hang or timeout
- Check if database is accessible
- Verify test database URL in conftest.py
- Check for infinite loops in code

---

## Success Indicators

### Phase 1 Complete When:
✅ Test database exists  
✅ All existing tests pass  
✅ Coverage report generated  
✅ No import or connection errors  

### Phase 2 Complete When:
✅ Coverage >80%  
✅ All API endpoints tested  
✅ All services tested  
✅ HTML coverage report shows green  

### Phase 3 Complete When:
✅ Initial migration created  
✅ Migration applies successfully  
✅ Migration rolls back successfully  
✅ Works on clean database  
✅ Seed script compatible  

### Phase 4 Complete When:
✅ Backend deployed to Cloud Run  
✅ Frontend deployed  
✅ Health check returns 200  
✅ API docs accessible  
✅ Can create/read data via API  

---

## Time Estimates

- **Phase 1:** 30-60 minutes
- **Phase 2:** 2-4 hours (depending on coverage gap)
- **Phase 3:** 1-2 hours
- **Phase 4:** 3-5 hours (first time), 1-2 hours (subsequent)

**Total:** 1-2 days for complete production readiness

---

## Notes

- Always test in Docker environment first
- Keep local environment working (don't break it)
- Commit after each successful phase
- Document any issues encountered
- Update STATUS.md after each phase
