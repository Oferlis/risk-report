using Microsoft.AspNetCore.Mvc;

namespace RiskReportService.Api.Health
{
    [ApiController]
    public class HealthController : ControllerBase
    {
        [HttpGet("/health")]
        public IActionResult GetHealth()
        {
            return Ok(new {Status = "available"});
        } 
    }
}